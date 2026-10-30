import unittest
import pandas as pd
from cohort import build

def inputs():
    f=pd.DataFrame([
        dict(survey='A',date='01/06/2024',site='Brighton',location='X',plant='P',**{'flowers probed ':4,'time flying (s)':10,'approx flower density (flowers / m2)':100}),
        dict(survey='A',date='01/06/2024',site='Brighton',location='X',plant='P',**{'flowers probed ':8,'time flying (s)':20,'approx flower density (flowers / m2)':100}),
        dict(survey='B',date='02/06/2024',site='Brighton',location='X',plant='P',**{'flowers probed ':6,'time flying (s)':15,'approx flower density (flowers / m2)':100})])
    n=pd.DataFrame([dict(survey=k,date=d,site='X',plant='P',**{'volume/flower':.1,'concentration':40,'tube volume':1,'tube length':64,'length':10,'number of flowers sampled':10}) for k,d in [('A','01/06/2024'),('B','02/06/2024')]])
    w=pd.DataFrame([dict(survey=k,date=d,site='Brighton',location='X',temperature=20,blue_sky=50,beaufort=2) for k,d in [('A','01/06/2024'),('B','02/06/2024')]])
    return f,n,w
class CohortTests(unittest.TestCase):
    def test_event_grain_is_not_weather_replication(self):
        d,q=build(*inputs());self.assertEqual(len(d),2);self.assertEqual(d.loc[d.survey=='A','probes'].iloc[0],6)
    def test_documented_imputed_nectar_excluded(self):
        f,n,w=inputs();n.loc[n.survey=='B','tube volume']=float('nan')
        d,q=build(f,n,w);self.assertEqual(list(d.survey),['A']);self.assertEqual(q['excluded'][0]['reason'],'nectar_not_directly_sampled')
    def test_conflicting_source_metadata_quarantined(self):
        f,n,w=inputs();n.loc[n.survey=='A','plant']='Q'
        d,q=build(f,n,w);self.assertEqual(list(d.survey),['B']);self.assertEqual(q['excluded'][0]['reason'],'nectar_metadata_mismatch')
    def test_repeated_weather_does_not_multiply_observations(self):
        f,n,w=inputs();w=pd.concat([w,w.iloc[:1]],ignore_index=True)
        d,q=build(f,n,w);self.assertEqual(len(d),2);self.assertEqual(q['forage_rows'],3)
if __name__=='__main__': unittest.main()
