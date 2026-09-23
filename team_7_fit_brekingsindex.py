#Schrijf zelf team_[nummer]_fit_brekingsindex.py. Het script moet:
#De meetdata inlezen (kolommen: hoek_graden, aantal_franjes, onzekerheid_N). Begin met jullie eigen team_[nummer]_data.csv, en later met team_[nummer]_metingen.csv zodra jullie zelf gemeten hebben met jullie eigen opstelling.
#De vergelijking die het aantal franjes N relateert aan de invalshoek (die jullie eerder hebben afgeleid) als Python-functie implementeren, met n als de te fitten parameter.
#Deze functie fitten op de meetdata om n (met onzekerheid) te bepalen. Gebruik hiervoor scipy.optimize.curve_fit; zoek zelf op hoe je deze functie aanroept en hoe je de onzekerheid uit het resultaat haalt.
#De gefitte waarde van n (met onzekerheid) printen.
#Een grafiek maken met de metingen (inclusief foutbalken) én de gefitte curve, met duidelijke assen en een legenda.
#De grafiek opslaan als team_[nummer]_fit_brekingsindex_plot.png.
#Denk na over welke parameters vast liggen (bekend) en welke je fit (onbekend), en over hoe je de onzekerheid op n interpreteert.

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# INSTELLINGEN TEAM 7

team_nummer = 7
bestandsnaam = "team_7_data.csv"

# Bekende parameters van de opstelling
d = 0.10          # Afstand tussen de spiegels in meter
lamda = 632.8e-9  # Golflengte laser in meter

# MEETDATA INLEZEN
# De CSV bevat de gemeten invalshoek, het aantal franjes
# en de onzekerheid op het aantal franjes.

data = np.genfromtxt(
    bestandsnaam,
    delimiter=",",
    names=True
)

hoek_graden = data["hoek_graden"]
N_gemeten = data["aantal_franjes"]
onzekerheid_N = data["onzekerheid_N"]

# Het punt bij 0 graden heeft een onzekerheid van 0.
# Dit punt wordt daarom niet meegenomen in de fit.
# Het kan wel in de uiteindelijke grafiek worden weergegeven.

fit_mask = onzekerheid_N > 0

hoek_graden_fit = hoek_graden[fit_mask]
N_gemeten_fit = N_gemeten[fit_mask]
onzekerheid_N_fit = onzekerheid_N[fit_mask]

hoek_rad_fit = np.deg2rad(hoek_graden_fit)

# THEORETISCH MODEL

def franjes_model(hoek, n):
    # Bereken het theoretische aantal franjes N
    # hoek = invalshoek
    # n = onbekende brekingsindex
    # Door breking verandert de optische weglengte.
    # Daardoor verandert de fase van het licht en ontstaan franjes.
    # Het aantal franjes N hangt af van de invalshoek en brekingsindex n.

    return (2 * d / lamda) * (
        np.sqrt(n**2 - np.sin(hoek)**2)
        - np.cos(hoek)
        + (1 - n)
    )

# FIT UITVOEREN

n_beginwaarde = 1.02
# Dit is alleen de beginwaarde voor de zoekprocedure.
# curve_fit bepaalt daarna zelf de best passende waarde van n.
# curve_fit zoekt de waarde van n waarvoor het model
# zo goed mogelijk overeenkomt met de meetgegevens.

popt, pcov = curve_fit(
    franjes_model,
    hoek_rad_fit,
    N_gemeten_fit,
    p0=[n_beginwaarde],
    sigma=onzekerheid_N_fit,
    absolute_sigma=True,
    bounds=([1.000001], [3.0]),
    maxfev=100000
)

n_fit = popt[0]
onzekerheid_n = np.sqrt(pcov[0, 0])

# RESULTAAT PRINTEN

print("FIT VAN DE BREKINGSINDEX - TEAM 7")

# Twee cijfers achter de komma
print(f"n = {n_fit:.4f} +/- {onzekerheid_n:.8f}")

# FITCURVE BEREKENEN

hoek_fit_graden = np.linspace(
    min(hoek_graden),
    max(hoek_graden),
    500
)

hoek_fit_rad = np.deg2rad(hoek_fit_graden)

N_fit = franjes_model(hoek_fit_rad, n_fit)

# GRAFIEK MAKEN

plt.figure(figsize=(9, 6))

plt.errorbar(
    hoek_graden,
    N_gemeten,
    yerr=onzekerheid_N,
    fmt="o",
    capsize=4,
    label="Meetdata team 7"
)

plt.plot(
    hoek_fit_graden,
    N_fit,
    label=f"Fit: n = {n_fit:.4f} +/- {onzekerheid_n:.8f}"
)

plt.xlabel("Invalshoek (graden)")
plt.ylabel("Aantal franjes N")
plt.title("Bepaling van de brekingsindex - Team 7")

plt.legend()
plt.grid(True)
plt.tight_layout()

# GRAFIEK OPSLAAN

plot_bestandsnaam = "team_7_fit_brekingsindex_plot.png"

plt.savefig(plot_bestandsnaam, dpi=300)

print(f"Grafiek opgeslagen als: {plot_bestandsnaam}")

plt.show()
