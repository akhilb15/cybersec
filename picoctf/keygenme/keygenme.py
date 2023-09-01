import hashlib
key_part_static1_trial = "picoCTF{1n_7h3_|<3y_of_"
key_part_static2_trial = "}"
bUsername_trial = b"SCHOFIELD"
s = hashlib.sha256(bUsername_trial).hexdigest()

print(key_part_static1_trial + s[4] + s[5] + s[3] + s[6] + s[2] + s[7] + s[1] + s[8] + key_part_static2_trial)
