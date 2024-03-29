
import json
import pandas as pd
import altair as alt

envs = ['gym_ant', 'gym_halfcheetah', 'gym_hopper', 'gym_humanoid', 'gym_inverteddoublependulum','gym_invertedpendulum','gym_reacher', 'gym_swimmer', 'gym_walker2d']
# Convert the data to JSON format
with open('data_run3.json') as f:
    data_json = json.load(fp=f)

data_df = pd.DataFrame(data_json)

data_df = data_df.groupby(['algorithm','env'])
data_df = data_df.rolling(2).mean().reset_index()


# Define the Vega chart
env_dropdown = alt.binding_select(options=envs, name='Env: ')
env_select = alt.selection_point(fields=['env'], bind=env_dropdown, value='gym_ant')

data_range = alt.binding_range(min=0.1, max=1.5, step=0.1, name='Range')
data_selector = alt.selection_point(
    name="SelectorName",
    fields=['Range'],
    bind=data_range,
    value=1.5,
)
alg_select = alt.selection_point(fields=['algorithm'], bind='legend')

base = alt.Chart(data_df).transform_calculate(
    rew_lower="datum.value_mean - datum.value_std",
    rew_upper="datum.value_mean + datum.value_std",
    tooltip_str="datum.value_mean + ' +/- ' + datum.value_std"
).add_params(alg_select).encode(x=alt.X('step:Q', title='RL Iterations (M)'), y=alt.Y('value_mean:Q', title='Total Reward'), 
         color=alt.Color('algorithm:N', title='Algorithm'),
         opacity=alt.condition(alg_select, alt.value(1), alt.value(0.3)))


area = base.mark_area().encode(y='rew_lower:Q', y2='rew_upper:Q', opacity=alt.condition(alg_select, alt.value(0.4), alt.value(0.0))).encode(tooltip=[alt.Tooltip('step:Q', title='RL Iterations (M)'),
                                        alt.Tooltip('algorithm:N', title='Algorithm'),
                                        alt.Tooltip('tooltip_str:N', title='Total Reward')])

line = base.mark_line().encode(tooltip=[alt.Tooltip('step:Q', title='RL Iterations (M)'),
                                        alt.Tooltip('algorithm:N', title='Algorithm'),
                                        alt.Tooltip('tooltip_str:N', title='Total Reward')])

chart = alt.layer(area, line).add_params(env_select).transform_filter(env_select).properties(width=600, height=400)
chart = chart.add_params(data_selector).transform_filter(alt.datum.step <= data_selector.Range)
chart = chart.configure_axisX(tickCount=10)

# chart = alt.Chart(pd.DataFrame(data_json)).mark_line().add_params(data_selector).transform_filter(alt.datum.step <= data_selector.Range)
# chart = chart.add_params(
#     env_select).transform_filter(env_select).encode(
#     x='step:Q',
#     y='value_mean:Q',
#     color='algorithm:N',
#     tooltip=['algorithm', 'step', 'value_mean'],
#     ).properties(width=400, height=300)
    
# Display the chart
chart.save('benchmark_run3_1.html')
