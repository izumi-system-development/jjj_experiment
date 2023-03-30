Theta_hs_out_max_H_d_t_limit: float = 45
"""最大暖房出力時の熱源機の出口における空気温度の最大値の上限値"""
Theta_hs_out_min_C_d_t_limit: float = 15
"""最大冷房出力時の熱源機の出口における空気温度の最低値の下限値"""
C_df_H_d_t_defrost_ductcentral: float = 0.77
"""デフロストに関する暖房出力補正係数（ダクトセントラル空調機）"""
defrost_temp_ductcentral: float = 5
"""デフロスト発生外気温度（ダクトセントラル空調機）"""
defrost_humid_ductcentral: float = 80
"""デフロスト発生外気相対湿度（ダクトセントラル空調機）"""
phi_i: float = 0.49
"""ダクトiの線熱損失係数"""
C_V_fan_dsgn_H: float = 0.79
"""暖房時の送風機の設計風量に関する係数"""
C_V_fan_dsgn_C: float = 0.79
"""冷房時の送風機の設計風量に関する係数"""
C_df_H_d_t_defrost_rac: float = 0.77
"""デフロストに関する暖房出力補正係数（ルームエアコンディショナー）"""
defrost_temp_rac: float = 5
"""デフロスト発生外気温度（ルームエアコンディショナー）"""
defrost_humid_rac: float = 80
"""デフロスト発生外気相対湿度（ルームエアコンディショナー）"""
C_hm_C: float = 1.15
"""室内機吸い込み湿度に関する冷房出力補正係数"""
q_rtd_C_limit: float = 5600
"""定格冷房能力の最大値"""
#以下、潜熱評価モデル追加対応(暖房)
A_f_hex_small_H: float = 0.2
"""定格冷却能力が5.6kW未満の場合のA_f,hex"""
A_e_hex_small_H: float = 6.2
"""定格冷却能力が5.6kW未満の場合のA_e,hex"""
A_f_hex_large_H: float = 0.3
"""定格冷却能力が5.6kW以上の場合のA_f,hex"""
A_e_hex_large_H: float = 10.6
"""定格冷却能力が5.6kW以上の場合のA_e,hex"""
a_c_hex_c_a1_H: float = 0.0631
"""熱伝達特性_a1"""
a_c_hex_c_a0_H: float = 0.0015
"""熱伝達特性_a0"""
a_r_H_t_t_a2: float = -0.0316
"""コンプレッサ効率特性_a2"""
a_r_H_t_t_a1: float = 0.2944
"""コンプレッサ効率特性_a1"""
airvolume_coeff_minimum_H: float = 0.17
"""風量特性_中間期及び最小風量"""
airvolume_coeff_a1_H: float = 0.092
"""風量特性_a1"""
airvolume_coeff_a2_H: float = -0.06
"""風量特性_a2"""
P_fan_H_d_t_a3: float = 1.4675
"""ファン消費電力_a3"""
P_fan_H_d_t_a2: float = 8.5886
"""ファン消費電力_a2"""
P_fan_H_d_t_a1: float = 20.217
"""ファン消費電力_a1"""
P_fan_H_d_t_a0: float = 50
"""ファン消費電力_a0"""
#以下、潜熱評価モデル追加対応(冷房)
A_f_hex_small_C: float = 0.2
"""定格冷却能力が5.6kW未満の場合のA_f,hex"""
A_e_hex_small_C: float = 6.2
"""定格冷却能力が5.6kW未満の場合のA_e,hex"""
A_f_hex_large_C: float = 0.3
"""定格冷却能力が5.6kW以上の場合のA_f,hex"""
A_e_hex_large_C: float = 10.6
"""定格冷却能力が5.6kW以上の場合のA_e,hex"""
a_c_hex_c_a1_C: float = 0.0631
"""熱伝達特性_a1"""
a_c_hex_c_a0_C: float = 0.0015
"""熱伝達特性_a0"""
a_r_C_d_t_a2: float = -0.0316
"""コンプレッサ効率特性_a2"""
a_r_C_d_t_a1: float = 0.2944
"""コンプレッサ効率特性_a1"""
airvolume_coeff_minimum_C: float = 0.17
"""風量特性_中間期及び最小風量"""
airvolume_coeff_a1_C: float = 0.092
"""風量特性_a1"""
airvolume_coeff_a2_C: float = -0.06
"""風量特性_a2"""
P_fan_C_d_t_a3: float = 1.4675
"""ファン消費電力_a3"""
P_fan_C_d_t_a2: float = 8.5886
"""ファン消費電力_a2"""
P_fan_C_d_t_a1: float = 20.217
"""ファン消費電力_a1"""
P_fan_C_d_t_a0: float = 50
"""ファン消費電力_a0"""


def set_constants(input: dict):
  if 'Theta_hs_out_max_H_d_t_limit' in input:
    global Theta_hs_out_max_H_d_t_limit
    Theta_hs_out_max_H_d_t_limit = float(input['Theta_hs_out_max_H_d_t_limit'])
  if 'Theta_hs_out_min_C_d_t_limit' in input:
    global Theta_hs_out_min_C_d_t_limit
    Theta_hs_out_min_C_d_t_limit = float(input['Theta_hs_out_min_C_d_t_limit'])
  if 'C_df_H_d_t_defrost_ductcentral' in input:
    global C_df_H_d_t_defrost_ductcentral
    C_df_H_d_t_defrost_ductcentral = float(input['C_df_H_d_t_defrost_ductcentral'])
  if 'defrost_temp_ductcentral' in input:
    global defrost_temp_ductcentral
    defrost_temp_ductcentral = float(input['defrost_temp_ductcentral'])
  if 'defrost_humid_ductcentral' in input:
    global defrost_humid_ductcentral
    defrost_humid_ductcentral = float(input['defrost_humid_ductcentral'])
  if 'phi_i' in input:
    global phi_i
    phi_i = float(input['phi_i'])
  if 'C_V_fan_dsgn_H' in input:
    global C_V_fan_dsgn_H
    C_V_fan_dsgn_H = float(input['C_V_fan_dsgn_H'])
  if 'C_V_fan_dsgn_C' in input:
    global C_V_fan_dsgn_C
    C_V_fan_dsgn_C = float(input['C_V_fan_dsgn_C'])
  if 'C_df_H_d_t_defrost_rac' in input:
    global C_df_H_d_t_defrost_rac
    C_df_H_d_t_defrost_rac = float(input['C_df_H_d_t_defrost_rac'])
  if 'defrost_temp_rac' in input:
    global defrost_temp_rac
    defrost_temp_rac = float(input['defrost_temp_rac'])
  if 'defrost_humid_rac' in input:
    global defrost_humid_rac
    defrost_humid_rac = float(input['defrost_humid_rac'])
  if 'C_hm_C' in input:
    global C_hm_C
    C_hm_C = float(input['C_hm_C'])
  if 'q_rtd_C_limit' in input:
    global q_rtd_C_limit
    q_rtd_C_limit = float(input['q_rtd_C_limit'])
  #以下、潜熱評価モデル追加対応
  if ['H_A']['A_f_hex_small'] in input:
    global A_f_hex_small_H
    A_f_hex_small_H = float(input['H_A']['A_f_hex_small'])
  if ['H_A']['A_e_hex_small'] in input:
    global A_e_hex_small_H
    A_e_hex_small_H = float(input['H_A']['A_e_hex_small'])
  if ['H_A']['A_f_hex_large'] in input:
    global A_f_hex_large_H
    A_f_hex_large_H = float(input['H_A']['A_f_hex_large'])
  if ['H_A']['A_e_hex_large'] in input:
    global A_e_hex_large_H
    A_e_hex_large_H = float(input['H_A']['A_e_hex_large'])
  if ['H_A']['coil_coeff'] in input:
    global a_c_hex_c_a1_H 
    a_c_hex_c_a1_H = float(input['H_A']['coil_coeff'][3])
    global a_c_hex_c_a0_H 
    a_c_hex_c_a0_H = float(input['H_A']['coil_coeff'][4])
  if ['H_A']['compressor_coeff'] in input:
    global a_r_H_t_t_a2 
    a_r_H_t_t_a2 = float(input['H_A']['compressor_coeff'][2])
    global a_r_H_t_t_a1 
    a_r_H_t_t_a1 = float(input['H_A']['compressor_coeff'][3])
  if ['H_A']['airvolume_coeff_minimum'] in input:
    global airvolume_coeff_minimum_H 
    airvolume_coeff_minimum_H = float(input['H_A']['airvolume_coeff_minimum'][0])
  if ['H_A']['airvolume_coeff'] in input:
    global airvolume_coeff_a1_H 
    airvolume_coeff_a1_H = float(input['H_A']['airvolume_coeff'][3])
    global airvolume_coeff_a0_H 
    airvolume_coeff_a0_H = float(input['H_A']['airvolume_coeff'][4])
  if ['H_A']['fan_coeff'] in input:
    global P_fan_H_d_t_a3 
    P_fan_H_d_t_a3 = float(input['H_A']['fan_coeff'][1])
    global P_fan_H_d_t_a2 
    P_fan_H_d_t_a2 = float(input['H_A']['fan_coeff'][2])
    global P_fan_H_d_t_a1 
    P_fan_H_d_t_a1 = float(input['H_A']['fan_coeff'][3])
    global P_fan_H_d_t_a0 
    P_fan_H_d_t_a0 = float(input['H_A']['fan_coeff'][4])
  if ['C_A']['A_f_hex_small'] in input:
    global A_f_hex_small_C
    A_f_hex_small_C = float(input['C_A']['A_f_hex_small'])
  if ['C_A']['A_e_hex_small'] in input:
    global A_e_hex_small_C
    A_e_hex_small_C = float(input['C_A']['A_e_hex_small'])
  if ['C_A']['A_f_hex_large'] in input:
    global A_f_hex_large_C
    A_f_hex_large_C = float(input['C_A']['A_f_hex_large'])
  if ['C_A']['A_e_hex_large'] in input:
    global A_e_hex_large_C
    A_e_hex_large_C = float(input['C_A']['A_e_hex_large'])
  if ['C_A']['coil_coeff'] in input:
    global a_c_hex_c_a1_C 
    a_c_hex_c_a1_C = float(input['C_A']['coil_coeff'][3])
    global a_c_hex_c_a0_C
    a_c_hex_c_a0_C = float(input['C_A']['coil_coeff'][4])
  if ['C_A']['compressor_coeff'] in input:
    global a_r_C_t_t_a2 
    a_r_C_t_t_a2 = float(input['C_A']['compressor_coeff'][2])
    global a_r_C_t_t_a1 
    a_r_C_t_t_a1 = float(input['C_A']['compressor_coeff'][3])
  if ['C_A']['airvolume_coeff_minimum'] in input:
    global airvolume_coeff_minimum_C 
    airvolume_coeff_minimum_C = float(input['C_A']['airvolume_coeff_minimum'][0])
  if ['C_A']['airvolume_coeff'] in input:
    global airvolume_coeff_a1_C 
    airvolume_coeff_a1_C = float(input['C_A']['airvolume_coeff'][3])
    global airvolume_coeff_a0_C 
    airvolume_coeff_a0_C = float(input['C_A']['airvolume_coeff'][4])
  if ['C_A']['fan_coeff'] in input:
    global P_fan_C_d_t_a3 
    P_fan_C_d_t_a3 = float(input['C_A']['fan_coeff'][1])
    global P_fan_C_d_t_a2 
    P_fan_C_d_t_a2 = float(input['C_A']['fan_coeff'][2])
    global P_fan_C_d_t_a1 
    P_fan_C_d_t_a1 = float(input['C_A']['fan_coeff'][3])
    global P_fan_C_d_t_a0 
    P_fan_C_d_t_a0 = float(input['C_A']['fan_coeff'][4])
    
