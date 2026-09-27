import json, base64, numpy as np, chaosmagpy as cp
import cartopy.feature as cfeature
m = cp.load_CHAOS_matfile('bruce/bruce/SA_DMD/chaosmagpy_package_0.14_0801/data/CHAOS-8.1.mat')
R = 3485.0
def mjd(y): 
    yi = int(np.floor(y)); mo = 1 + int(round((y - yi) * 12)); return cp.data_utils.mjd2000(yi, mo, 1)
def q8(a, vmax): return base64.b64encode(np.clip(np.round(a / vmax * 127), -127, 127).astype(np.int8).tobytes()).decode()

# polar maps
years = np.round(np.arange(2000.0, 2025.01, 0.5), 2)
colat = np.arange(0, 62.1, 2.0); lon = np.arange(0, 360, 4.0)
maps = np.array([m.synth_values_tdep(mjd(y), R, colat, lon, nmax=16, deriv=2, grid=True)[0] for y in years]) / 1000.0
vmap = float(np.percentile(np.abs(maps), 99.5))
# hovmoller sections
hy = np.round(np.arange(2000.0, 2025.01, 0.25), 2); hl = np.arange(60, 270.1, 2.0); lats = [60, 70, 80]
hov = {str(la): np.array([m.synth_values_tdep(mjd(y), R, 90.0 - la, hl, nmax=16, deriv=2)[0] for y in hy]) / 1000.0 for la in lats}
vhov = float(np.percentile(np.abs(np.concatenate([h.ravel() for h in hov.values()])), 99.5))
# coastlines north of 20N
coast = []
for g in cfeature.COASTLINE.with_scale('110m').geometries():
    for line in getattr(g, 'geoms', [g]):
        xy = np.array(line.coords)
        seg = []
        for x, y in xy:
            if y >= 20: seg.append([round(float(x), 1), round(float(y), 1)])
            elif len(seg) > 1: coast.append(seg); seg = []
            else: seg = []
        if len(seg) > 1: coast.append(seg)
out = dict(model='CHAOS-8.1', radius_km=R, nmax=16, units='uT/yr^2',
           map=dict(years=years.tolist(), colat=colat.tolist(), lon=lon.tolist(), vmax=round(vmap, 3), data=q8(maps, vmap)),
           hov=dict(years=hy.tolist(), lon=hl.tolist(), lats=lats, vmax=round(vhov, 3), data={k: q8(v, vhov) for k, v in hov.items()}),
           coast=coast)
json.dump(out, open('figs/chaos81_cmb.json', 'w'), separators=(',', ':'))
print(maps.shape, vmap, vhov, len(coast), sum(len(c) for c in coast))
