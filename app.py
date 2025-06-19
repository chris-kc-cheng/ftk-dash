import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc

# Data
print("Loading data...")


# App
app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.FONT_AWESOME]
)

server = app.server

app.layout = html.Div([
    dbc.Navbar(
        dbc.Container([
            dbc.Row([
                dbc.Col(dbc.NavbarBrand(
                    "Market Monitor Dashboard", className="ms-2")),
            ]),
            dbc.Nav([
                dbc.Col(dbc.NavItem(dbc.NavLink("MSCI RT", href="/", className="text-nowrap"))),
                dbc.Col(dbc.NavItem(dbc.NavLink("World Indices", href="/wei", className="text-nowrap"))),
                dbc.DropdownMenu(
                    [
                        dbc.Switch(
                            id="switch", value=True, className="d-inline-block ms-1", persistence=True)
                    ],
                    label=dbc.Label(className="fa fa-gear", html_for="switch")
                )
            ]),
        ]),
        color="primary",
        dark=True,
    ),
    dbc.Container([
        dash.page_container
    ])
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
