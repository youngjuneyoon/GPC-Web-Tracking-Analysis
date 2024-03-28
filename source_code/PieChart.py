import plotly.graph_objects as go

colors = ['orange', 'gray']

labels = ["Tracking Domain", "Regular Domain"]
values = [18100, 5634]

fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
fig.update_traces(marker=dict(colors=colors))
fig.show()

labels = ["Tracking Domain", "Regular Domain"]
values = [20522, 7646]

fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
fig.update_traces(marker=dict(colors=colors))


fig.show()
