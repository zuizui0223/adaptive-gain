"""Synthetic exact weather-forecast timing grid and machine-readable receipt."""
from fractions import Fraction as F
from pathlib import Path
import argparse,csv,json
from adaptive_gain.wind_forecast_routing import forecast_accuracy

MIX=((3,F(1,2)),(7,F(1,2)))
COST=((1,1),(1,2))
SCHEDULES={
 "no_forecast":(),
 "tick_0_only":(0,),
 "tick_1_only":(1,),
 "tick_4_only":(4,),
 "ticks_1_and_4":(1,4),
 "continuous":tuple(range(7)),
 "from_tick_2":tuple(range(2,7)),
}


def main(folder):
    out=Path(folder);out.mkdir(parents=True,exist_ok=True)
    rows=[];sweep={}
    for p in (F(1,10),F(1,2),F(9,10)):
        per_noise={}
        for noise in (F(0),F(1,10),F(1,4),F(1,2)):
            v={}
            for schedule,ticks in SCHEDULES.items():
                score=forecast_accuracy(MIX,4,(0,1),source_costs=COST,
                      stay=p,forecast_error=noise,forecast_ticks=ticks)
                v[schedule]=score
                rows.append({"wind_persistence":str(p),"forecast_error":str(noise),
                     "availability":schedule,"accuracy_exact":str(score),
                     "accuracy_percent":f"{float(score)*100:.9f}"})
            baseline=v["no_forecast"];total=v["continuous"]-baseline
            assert v["tick_0_only"]==baseline
            assert v["ticks_1_and_4"]==v["continuous"]
            assert v["tick_1_only"]-baseline>=F(99,100)*total
            per_noise[str(noise)]={
              "baseline":str(baseline),"continuous":str(v["continuous"]),
              "single_tick_1":str(v["tick_1_only"]),
              "two_forecasts_at_1_4":str(v["ticks_1_and_4"]),
              "t1_share_of_total":str((v["tick_1_only"]-baseline)/total) if total else None,
              "total_forecast_gain_pp":float(total*100),
              "gain_t1_pp":float((v["tick_1_only"]-baseline)*100)}
        sweep[str(p)]=per_noise
    assert len(rows)==84
    with (out/"timing_grid.csv").open("w",newline="",encoding="utf-8") as fh:
        writer=csv.DictWriter(fh,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)
    receipt={"scope":"SYNTHETIC_32_WORLD_BAYESIAN_TASK_NOT_FIELD_FIT",
      "worlds":32,"resource_branches":16,
      "deadline_distribution":[[3,"1/2"],[7,"1/2"]],
      "weather_survival":{"calm":"19/20","gust":"13/20"},
      "heterospecific_source_error":"1/10",
      "source_cost":{"calm":[1,1],"gust":[1,2]},
      "grid_rows":len(rows),"wind_persistence":sweep,
      "claim_ceiling":"Information decision accuracy only, not ecological fitness or measured animal behavior"}
    (out/"summary.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2),
                                  encoding="utf-8")
    print("EXACT_FORECAST_TIMING_GRID_PASS",len(rows),
          json.dumps(sweep["1/2"]["0"],ensure_ascii=False))
    return receipt


if __name__=="__main__":
    cli=argparse.ArgumentParser()
    cli.add_argument("--out",default="wind_timing_results")
    args=cli.parse_args()
    main(args.out)
