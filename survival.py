import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter

fp=open("dataset.tsv")
header=next(fp)
header=header.strip().split("\t")
events=[]
duration=[]
days_to_death_index=header.index("days_to_death")
days_to_last_follow_up_index=header.index("days_to_last_follow_up")
for line in fp:
    arr=line.strip().split("\t")
    days_to_death=arr[days_to_death_index]
    days_to_last_follow_up=arr[days_to_last_follow_up_index]
    if days_to_death=="-1":
        if days_to_last_follow_up!="-1":
            duration.append(int(days_to_last_follow_up))
            events.append(0)
        else:
            print("[SKIP]")
    else:
        duration.append(int(days_to_death))
        events.append(1)

print(duration)
print(events)

kmf = KaplanMeierFitter(label="sample")
kmf.fit(duration,events)
kmf.plot()
plt.savefig("km.png")
