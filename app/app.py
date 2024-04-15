#Imports

import seaborn as sns
from faicons import icon_svg
from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins 
import plotly.express as px
import shinyswatch
import pandas as pd
from shinywidgets import render_plotly

#loading penguins dataset
df = palmerpenguins.load_penguins()

# Theme
shinyswatch.theme.superhero()

## names the page
ui.page_opts(title="Penguins dashboard",  fillable=True)

# creating filter 
with ui.sidebar(title="Filter controls"):
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)

 #creating a numeric input for the number of Plotly histogram bins
   # ui.input_numeric("plotly_bin_count", "Number of Plotly bins", 45)

# creating a checkbox group input
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )

# Adding a hyperlink 
    ui.hr()
    ui.h6("Links")
    ui.a(
        "GitHub Source",
        href="https://github.com/anjana-codes/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://anjana-codes.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/anjana-codes/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

#Creating layout columns for displaying penguin statistics
with ui.layout_column_wrap(fill=False):
   with ui.value_box(showcase=icon_svg("snowman"),width="50px", theme="bg-gradient-green-blue"
                             ):
        "Number of  Penguins"

        @render.text
        def count():
            return filtered_df().shape[0]
            
# Value box to display average bill length
   with ui.value_box(showcase=icon_svg("ruler-horizontal"), theme="bg-gradient-blue-purple"
        ):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"
            
 # Value box to display average bill depth
   with ui.value_box(showcase=icon_svg("ruler-vertical"), theme="bg-gradient-blue-purple"
                    ):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

# Creating layout columns for displaying plots and data frames
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.h2("Plotly Histogram: Species")

        @render_plotly
        def length_depth_plotly():
            return px.histogram(
                data_frame=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                color="species",
                color_discrete_map={
                     'Adelie': 'yellow',
                     'Chinstrap': 'brown',
                     'Gentoo': 'green'} 
            )
#changing data grid header
    with ui.card(full_screen=True):
        ui.card_header("Penguin Data")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)


#ui.include_css(app_dir / "styles.css")

# Reactive calculation to filter data based on selected species 

@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
