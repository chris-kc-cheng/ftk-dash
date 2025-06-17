import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])

color_mode_switch = html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="switch"),
        dbc.Switch( id="switch", value=True, className="d-inline-block ms-1", persistence=True),        
        dbc.Label(className="fa fa-sun", html_for="switch"),
    ]
)

app.layout = html.Div([
    html.H1('Multi-page app with Dash Pages'),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    color_mode_switch,
    dash.page_container
])

dash.clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute("data-bs-theme", switchOn ? "light" : "dark");
       return window.dash_clientside.no_update
    }
    """,
    dash.Output("switch", "id"),
    dash.Input("switch", "value"),
)

if __name__ == '__main__':
    app.run(debug=True)