import json, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
import cartopy.crs as ccrs, cartopy.feature as cfeature
import chaosmagpy as cp

BLUE, PAPER, RED, GREY = '#2E5B78', '#F4F5F2', '#C3352B', '#8A929C'
cmap = LinearSegmentedColormap.from_list('site', ['#1F4058', BLUE, '#9DB7C8', '#F1F2EE', '#E3A79F', RED, '#8E2119'])
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'text.color':GREY,'axes.labelcolor':GREY,'xtick.color':GREY,'ytick.color':GREY,'axes.edgecolor':GREY})
W, H, DPI = 8, 6, 150   # 1200x900 px, 4:3

m = cp.load_CHAOS_matfile('bruce/bruce/SA_DMD/chaosmagpy_package_0.14_0801/data/CHAOS-8.1.mat')
R = 3485.0

# ---- A: radial secular acceleration at the CMB, north polar view, 2015.0 ----
t = cp.data_utils.mjd2000(2015, 1, 1)
th = np.linspace(0.0, 64, 160); ph = np.linspace(-180, 180, 361)
Br = m.synth_values_tdep(t, R, th, ph, nmax=16, deriv=2, grid=True)[0] / 1000.0  # uT/yr^2
v = np.percentile(np.abs(Br), 99)
fig = plt.figure(figsize=(W, H), dpi=DPI)
import matplotlib.path as mpath
ax = fig.add_axes([0.125, 0.02, 0.75, 0.96], projection=ccrs.NorthPolarStereo(central_longitude=-150))
ax.set_extent([-180, 180, 30, 90], ccrs.PlateCarree())
circ = mpath.Path(np.vstack([np.sin(np.linspace(0, 2*np.pi, 200)), np.cos(np.linspace(0, 2*np.pi, 200))]).T * .5 + .5)
ax.set_boundary(circ, transform=ax.transAxes)
P, T = np.meshgrid(ph, 90 - th)
ax.contourf(P, T, Br, levels=np.linspace(-v, v, 17), cmap=cmap, extend='both', transform=ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE.with_scale('110m'), linewidth=.5, edgecolor='#4A5058', alpha=.7)
ax.gridlines(color=GREY, linewidth=.3, alpha=.5, xlocs=range(-180, 180, 30), ylocs=[30, 50, 70])
ax.spines['geo'].set_edgecolor(GREY); ax.spines['geo'].set_linewidth(.6)
fig.savefig('figs/core_sa_polar.png', transparent=True); plt.close(fig)

# ---- B: longitude-time (Hovmoller) of SA at 70N on the CMB ----
years = np.arange(2001.0, 2024.51, 0.25)
ts = np.array([cp.data_utils.mjd2000(int(y), 1 + int(round((y % 1) * 12)), 1) for y in years])
lon = np.linspace(80, 250, 171)
H2 = np.array([m.synth_values_tdep(tt, R, 20.0, lon, nmax=16, deriv=2)[0] for tt in ts]) / 1000.0
v2 = np.percentile(np.abs(H2), 99)
fig, ax = plt.subplots(figsize=(W, H), dpi=DPI)
fig.subplots_adjust(left=.11, right=.97, bottom=.1, top=.97)
ax.contourf(lon, years, H2, levels=np.linspace(-v2, v2, 17), cmap=cmap, extend='both')
ax.set_xlabel('Longitude (°E)'); ax.set_ylabel('Year')
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.tick_params(length=3, width=.6)
fig.savefig('figs/sa_hovmoller.png', transparent=True); plt.close(fig)

# ---- C: MDJ record of the 2017-09-03 DPRK test with P pick ----
S = json.load(open('mdj.json')); y = np.array(S['y']); tt = S['t_origin'] + np.linspace(0, S['dur'], len(y))
yc = np.sign(y) * np.abs(y) ** .55
fig, ax = plt.subplots(figsize=(W, H), dpi=DPI)
fig.subplots_adjust(left=.04, right=.98, bottom=.1, top=.97)
ax.plot(tt, yc, color='#161A20', lw=.6)
tp = S['t_origin'] + S['pick']
ax.axvline(tp, color=RED, lw=.9, ls=(0, (2, 3))); ax.text(tp + 1.5, 1.02, 'P', color=RED, fontsize=11, va='top', weight='bold')
ax.set_ylim(-1.1, 1.1); ax.set_yticks([]); ax.set_xlabel('Seconds after origin')
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.tick_params(length=3, width=.6)
fig.savefig('figs/mdj_waveform.png', transparent=True); plt.close(fig)
print('ok', v, v2)
