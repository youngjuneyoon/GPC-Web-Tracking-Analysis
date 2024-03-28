import plotly.graph_objects as go

# HTTP REQUEST - All
types=['St. Louis', 'Los Angeles', 'Germany']
t2 = [125899, 119075, 81888]
t3 = [110159 , 102072, 81089]
fig = go.Figure(data=[
    go.Bar(name='Baseline', x=types, y=t2, text = t2),
    go.Bar(name='GPC Enabled', x=types, y=t3, text = t3)
])
# Change the bar mode
fig.update_layout(
    barmode='group',
    title_text='All HTTP Requests Counts',
    xaxis_title="Region",
    yaxis_title="# of HTTP Requests",
    )

fig.show()


# HTTP REQUEST - Tracker
types=['St. Louis', 'Los Angeles', "Germany"]
t2 = [57359, 52674, 25520]
t3 = [46716, 39990, 25299]
fig = go.Figure(data=[
    go.Bar(name='Baseline', x=types, y=t2, text = t2),
    go.Bar(name='GPC Enabled', x=types, y=t3, text = t3)
])
# Change the bar mode
fig.update_layout(
    barmode='group',
    title_text='HTTP Requests Counts - Tracker Domain',
    xaxis_title="Region",
    yaxis_title="# of HTTP Requests",
    )

fig.show()


# Cookies - All
types=['St. Louis', 'Los Angeles', 'Germany']
t2 = [85928 + 15484, 80993 + 14541, 33916 + 7121]
t3 = [65547 + 12131, 56569 + 10797, 33635 + 7045]
fig = go.Figure(data=[
    go.Bar(name='Baseline', x=types, y=t2, text = t2),
    go.Bar(name='GPC Enabled', x=types, y=t3, text = t3)
])
# Change the bar mode
fig.update_layout(
    barmode='group',
    title_text='All Cookies Count',
    xaxis_title="Region",
    yaxis_title="# of cookies",
    )

fig.show()

# Cookies - Tracker
types=['St. Louis', 'Los Angeles', 'Germany']
t2 = [45092 + 8732, 39902 + 7722, 9722 + 2062]
t3 = [29769 + 5955, 22400 + 4702, 9752 + 2038]
fig = go.Figure(data=[
    go.Bar(name='Baseline', x=types, y=t2, text = t2),
    go.Bar(name='GPC Enabled', x=types, y=t3, text = t3)
])
# Change the bar mode
fig.update_layout(
    barmode='group',
    title_text='Cookies Count - Tracker Domain',
    xaxis_title="Region",
    yaxis_title="# of cookies",
    )

fig.show()