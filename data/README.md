# Data

All files needed to reproduce the paper's figures are included here (≈9 MB).
They are small extracts of public datasets, prepared for this study; please
cite the original sources listed below if you reuse them.

| Folder | File | Rows | Description |
|---|---|---|---|
| `ngsim/` | `stop_to_go.csv` | 8,166 | 16 leader–follower stop-and-go car-following trajectories extracted from NGSIM, sampled at 0.1 s. Columns: `Time`, `LD_position(m)`, `position(m)`, `LD_speed(m/s)`, `speed(m/s)`, `LD_acc(m/s^2)`, `acc(m/s^2)`, `No. of Trajectory`, `spacing (m)`. `LD_` = leader; unprefixed = follower. |
| `tgsim/` | `hdv_traj_i395.csv` | 222,477 | 524 human-driven vehicle (HDV) trajectories on I-395 from TGSIM (Kalman-filtered `xloc_kf`, `yloc_kf`, `speed_kf`, `acceleration_kf`; 0.1 s). |
| `tgsim/` | `av_traj_i395.csv` | 1,172 | 2 automated-vehicle (AV) trajectories on I-395 from TGSIM, same fields plus lane, dimensions and type. |
| `tgsim/` | `bus_traj_i395.csv` | 519 | 1 bus trajectory (TGSIM I-395), provided for extensions; not used in the paper's figures. |
| `tgsim/` | `truck_traj_i395.csv` | 474 | 1 truck trajectory (TGSIM I-395), provided for extensions; not used in the paper's figures. |
| `tgsim/` | `ped_traj_fb.csv` | 464 | 5 pedestrian trajectories (TGSIM Foggy Bottom) with x/y speed and acceleration, provided for extensions. Fig. 15b in the paper is produced from **synthetic** pedestrian profiles generated inside notebook 09. |
| `synthetic/` | `behavioral_transfer_data.xlsx` | 400 | 60-s speed profiles used by notebook 10 (Fig. 12): `Time`, `Leader_Speed`, `HDV_Speed`, `AV_Speed`. The leader and baseline AV are from a TGSIM I-395 stop-and-go episode with an HDV leader and AV follower; the target HDV is generated with the Asymmetric Behavioral (AB) model (Chen et al., 2012). |

## Original sources

* **NGSIM** — Next Generation Simulation program, U.S. Federal Highway Administration.
  <https://data.transportation.gov/Automobiles/Next-Generation-Simulation-NGSIM-Vehicle-Trajectori/8ect-6jqj>
* **TGSIM** — Third Generation Simulation Data, U.S. Federal Highway Administration
  (I-395 and Foggy Bottom sites). <https://data.transportation.gov/browse?q=TGSIM>

Terms of use of the original datasets apply to the extracts in this folder.
