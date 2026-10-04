#!/bin/sh
# Tạo Tong_hop_3_giao_trinh_D1_D2_KY_v4.html từ file v3: fz → ld → ky (các bài sinh từ md)
set -e
cd "$(dirname "$0")/.."
V3=Tong_hop_3_giao_trinh_D1_D2_KY_v3_Bai11_day_du.html
python3 tools/normalize_ky_md.py >/dev/null
python3 tools/sync_fz.py $V3 /tmp/_v4_a.html
python3 tools/sync_ld.py /tmp/_v4_a.html /tmp/_v4_b.html
python3 tools/ld_sentences.py /tmp/_v4_b.html
python3 tools/reorder_kb.py /tmp/_v4_b.html /tmp/_v4_c.html
python3 tools/gen_ky.py /tmp/_v4_c.html Tong_hop_3_giao_trinh_D1_D2_KY_v4.html ${@:-4}
python3 tools/link_kb.py Tong_hop_3_giao_trinh_D1_D2_KY_v4.html
python3 tools/link_tonghop.py Tong_hop_3_giao_trinh_D1_D2_KY_v4.html
python3 tools/rekey.py Tong_hop_3_giao_trinh_D1_D2_KY_v4.html
python3 tools/fix_ans_layout.py Tong_hop_3_giao_trinh_D1_D2_KY_v4.html
python3 tools/fz_cardui.py Tong_hop_3_giao_trinh_D1_D2_KY_v4.html
python3 tools/fz_pair.py Tong_hop_3_giao_trinh_D1_D2_KY_v4.html
python3 tools/ky_cardui.py Tong_hop_3_giao_trinh_D1_D2_KY_v4.html
python3 tools/ld_tools.py Tong_hop_3_giao_trinh_D1_D2_KY_v4.html
python3 tools/add_method.py Tong_hop_3_giao_trinh_D1_D2_KY_v4.html
python3 tools/add_relations.py Tong_hop_3_giao_trinh_D1_D2_KY_v4.html
