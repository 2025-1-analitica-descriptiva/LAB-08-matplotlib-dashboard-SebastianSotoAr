# pylint: disable=line-too-long
"""
Escriba el codigo que ejecute la accion solicitada.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

def pregunta_01():
    """
    El archivo `files//shipping-data.csv` contiene información sobre los envios
    de productos de una empresa. Cree un dashboard estático en HTML que
    permita visualizar los siguientes campos:

    * `Warehouse_block`

    * `Mode_of_Shipment`

    * `Customer_rating`

    * `Weight_in_gms`

    El dashboard generado debe ser similar a este:

    https://github.com/jdvelasq/LAB_matplotlib_dashboard/blob/main/shipping-dashboard-example.png

    Para ello, siga las instrucciones dadas en el siguiente video:

    https://youtu.be/AgbWALiAGVo

    Tenga en cuenta los siguientes cambios respecto al video:

    * El archivo de datos se encuentra en la carpeta `data`.

    * Todos los archivos debe ser creados en la carpeta `docs`.

    * Su código debe crear la carpeta `docs` si no existe.

    """

    output_dir = "docs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    input_file = "files/input/shipping-data.csv"
    df = pd.read_csv(input_file)

    # --- ♂Warehouse_block ---
    df_copy = df.copy()
    plt.Figure()

    counts = df_copy.Warehouse_block.value_counts()
    counts.plot.bar(
        title = "Shipping per Warehouse",
        xlabel = "Warehouse block",
        ylabel = "Record Count",
        color = "tab:blue",
        fontsize = 8
    )
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)

    plt.savefig(output_dir + "/shipping_per_warehouse.png")

    # --- ♂Mode_of_Shipment ---
    df_copy = df.copy()
    plt.figure()
    counts = df_copy["Mode_of_Shipment"].value_counts()
    counts.plot.pie(
        title="Mode of Shipment",
        wedgeprops={"width": 0.35},
        xlabel="Mode of Shipment",
        ylabel="",
        color=["tab:blue", "tab:orange", "tab:green", "tab:red"],
    )
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.savefig(output_dir + "/mode_of_shipment.png")

    # --- ♂Customer_rating ---
    df_copy = df.copy()
    plt.figure()
    df_copy = (
        df_copy[["Mode_of_Shipment", "Customer_rating"]]
        .groupby("Mode_of_Shipment")
        .describe()
    )
    df_copy.columns = df_copy.columns.droplevel(0)
    df_copy = df_copy[["mean","min","max"]]
    plt.barh(
        y=df_copy.index.values,
        width = df_copy['max'].values - 1,
        left = df_copy['min'].values,
        height = 0.9,
        color = "lightgray",
        alpha = 0.8,
    )
    colors = [
        "tab:green" if value >= 3.0 else "tab:orange" for value in df_copy["mean"].values
    ]
    plt.barh(
        y=df_copy.index.values,
        width=df_copy["mean"].values,
        left=df_copy["min"].values,
        height=0.5,
        color=colors,
        alpha=1.0,
    )
    plt.title("Average Customer Rating")
    plt.gca().spines["left"].set_color("gray")
    plt.gca().spines["bottom"].set_color("gray")
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.savefig(output_dir + "/average_customer_rating.png")

    # --- ♂Weight_in_gms ---
    df_copy = df.copy()
    plt.figure()
    df_copy["Weight_in_gms"].plot.hist(
        title="Shipped Weight Distribution",
        color="tab:orange",
        edgecolor="white",
    )
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.savefig(output_dir + "/weight_distribution.png")

    # --- ♂Dashboard HTML ---
    html = """
    <html>
      <head>
        <title>Dashboard de Envíos</title>
        <style>
          body { font-family: Arial, sans-serif; background: #fafafa; }
          h1 { text-align: center; }
          .grid { display: flex; flex-wrap: wrap; justify-content: center; gap: 40px; }
          .card { background: #fff; border-radius: 12px; box-shadow: 0 2px 8px #ccc; padding: 20px; margin: 10px; }
          .card img { display: block; margin: 0 auto 10px auto; max-width: 350px; }
          .caption { text-align: center; font-weight: bold; }
        </style>
      </head>
      <body>
        <h1>Dashboard de Envíos</h1>
        <div class="grid">
          <div class="card">
            <img src="shipping_per_warehouse.png" alt="Envíos por Warehouse Block">
            <div class="caption">Envíos por Warehouse Block</div>
          </div>
          <div class="card">
            <img src="mode_of_shipment.png" alt="Modo de Envío">
            <div class="caption">Modo de Envío</div>
          </div>
          <div class="card">
            <img src="average_customer_rating.png" alt="Rating Promedio">
            <div class="caption">Rating Promedio por Modo de Envío</div>
          </div>
          <div class="card">
            <img src="weight_distribution.png" alt="Distribución de Peso">
            <div class="caption">Distribución de Peso (g)</div>
          </div>
        </div>
      </body>
    </html>
    """
    
    with open(output_dir + "/index.html", "w", encoding="utf-8") as file:
        file.write(html)