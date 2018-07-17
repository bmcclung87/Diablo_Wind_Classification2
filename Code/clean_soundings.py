#load the sounding data already parsed out by season
fall_soundings = pickle.load(open(pickle_dir+'Fall_OAK_soundings.p','rb'))
summer_soundings = pickle.load(open(pickle_dir+'Summer_OAK_soundings.p','rb'))
spring_soundings = pickle.load(open(pickle_dir+'Spring_OAK_soundings.p','rb'))
winter_soundings = pickle.load(open(pickle_dir+'Winter_OAK_soundings.p','rb'))

#concatenate for easy searching
all_soundings = pd.concat([fall_soundings,summer_soundings,spring_soundings,winter_soundings])
all_u, all_v = mpcalc.get_wind_components(all_soundings[' Spd'].values*units.knots, \
                                         all_soundings[' Dir '].values*units.degrees)
all_soundings['U'] = all_u
all_soundings['V'] = all_v
all_soundings[' Dewpt'] = calc_dewpt(convert_temperature(all_soundings[' Temp'],'F','C'),all_soundings[' RH'])
all_soundings[' Temp'] = convert_temperature(all_soundings[' Temp'],'F','C')
all_soundings = all_soundings.rename(columns={' Month':'Month',' Day':'Day',\
                                              ' Hour':'Hour', ' Hgt': 'Hgt',\
                                              ' Pres':'Pres',' Temp':'Temp',\
                                              ' Dewpt':'Dewpt',' RH':'RH',\
                                              ' Spd':'Spd',' Dir ': 'Dir'})
pickle.dump(all_soundings,open(pickle_dir+'OAK_master.p','wb'))