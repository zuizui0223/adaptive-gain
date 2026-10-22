"""Cross-check the two source-locked wind experimental analyses with alternate estimators."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

ROOT=Path(__file__).parent
RESULTS=ROOT/'field_results'/'summary.json'
SWITCH=ROOT/'Balfouretal_Inflorescence_Switch_Rate_DataDryad.csv'
FLIGHTS=ROOT/'Bee_route_choice_in_wind.csv'

def run():
    s=pd.read_csv(SWITCH)
    s['Flower_species']=s['Flower_species'].str.strip()
    s['Bee_species']=s['Bee_species'].str.strip()
    s['Date']=s['Date'].str.strip()
    s['Location']=s['Location'].str.strip()
    s['log_I']=np.log(s['Inflorences'])
    s['log_F']=np.log(s['Flowers'])
    s['log_ratio']=s['log_I']-s['log_F']
    f=json.loads(RESULTS.read_text())['switch']
    audit={'statsmodels_direct':{},'leave_one_date_out':{},'source_sha256':hashlib.sha256(SWITCH.read_bytes()).hexdigest()}
    expr='Q("Wind")+C(Bee_species)+C(Flower_species)+C(Date)+Temp+C(Location)'
    for key,outcome in [('log_inflorescences_visited','log_I'),('log_flowers_visited','log_F'),('log_inflorescence_per_flower','log_ratio')]:
        model=smf.ols(f'{outcome} ~ {expr}',data=s).fit()
        coef=float(model.params['Q("Wind")'])
        audit['statsmodels_direct'][key]={'beta':coef,'original_beta':f[key]['wind_slope_log_per_ms'],
                                         'absolute_difference':abs(coef-f[key]['wind_slope_log_per_ms'])}
        leave=[]
        for date in s['Date'].unique():
            m=smf.ols(f'{outcome} ~ {expr}',data=s.loc[s['Date']!=date]).fit()
            leave.append(float(m.params['Q("Wind")']))
        audit['leave_one_date_out'][key]={'n_dates':len(leave),'min_beta':min(leave),'max_beta':max(leave),
                                          'all_positive':all(x>0 for x in leave),'all_negative':all(x<0 for x in leave)}
    # Directly and independently compute original controlled experiment within-bee-and-direction mean deltas.
    d=pd.read_csv(FLIGHTS)
    d['above']=(d['Median altitude (mm)']>d['Canopy height (mm)']).astype(float)
    route=json.loads((ROOT/'results'/'summary.json').read_text())['results']
    audit['flight_paired']={}
    for name,c,x in [('route_69to127','above',d[d['Canopy height (mm)']>=69]),
                     ('median_ground_speed','Median ground speed (m/s)',d),
                     ('lateral_excursion','Lateral excursion (mm)',d),
                     ('ground_speed_down_tailwind','Median ground speed (m/s)',d[d['Flight Direction Label']=='Down-tunnel'])]:
        p=x.pivot_table(index=['Bee ID','Flight Direction Label'],columns='Wind Presence',values=c,aggfunc='mean').dropna(subset=['Yes','No'])
        beta=float((p['Yes']-p['No']).groupby(level='Bee ID').mean().mean())
        audit['flight_paired'][name]={'beta':beta,'diff':abs(beta-route[name]['mean_wind_minus_still'])}
    errs=[v['absolute_difference'] for v in audit['statsmodels_direct'].values()]+[v['diff'] for v in audit['flight_paired'].values()]
    audit['max_absolute_discrepancy']=max(errs)
    assert audit['max_absolute_discrepancy']<1e-9
    (ROOT/'independent_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
    print(json.dumps(audit,indent=2,ensure_ascii=False))
    return audit
if __name__=='__main__':run()