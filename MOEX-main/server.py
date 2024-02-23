from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, Request

from ml import algos

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


a = '''45.503947663846375
45.561294233465844
45.592073431174526
45.95153902309803
45.84533409574469
45.88410132393327
45.865868706848254
45.76766585899416
45.7427724185588
45.880068671097824
45.96409563680738
45.88502699568029
45.67231172007735
45.54763280980885
45.48638159703976
45.58540953281288
45.35696494519464
45.653960147161825
45.649248653413295
45.61956409067408
45.46664944215871
45.524321817261075
45.66884080031944
45.64677471664824
45.91605416413107
45.903514604003774
45.8087299326798
46.055030630367355
46.08010026963575
46.28493036304571
46.489054818324476
46.42023066334951
46.3934528866311
46.6084719496944
46.57809480076572
46.308035367668296
46.46972402130819
46.37893048542235
46.18156725581458
46.42568187276058
46.17505441444949
46.14901380613397
46.18956705067554
46.20114149176759
46.022184288740135
46.12966071861975
46.1193049674487
45.749577583648026
45.625534389940995
45.66655966051681
45.66417899567558
45.827278723636766
45.765304607819914
45.7701952977483
45.90679776886819
45.74590031890763
45.62749597068969
45.869035521272316
45.84479160340841
45.818950581057216
45.95128068015392
46.202871283147765
46.165085827979496
46.1394499779913
46.04147390782456
46.091498907518506
46.128962580847556
46.12694063431857
45.99865718851454
45.85552781382116
45.825785644498474
45.64443823167385
45.550645089916564
45.58126810999268
45.54976941140537
45.53250252913509
45.190183255307005
45.25470820896023
45.089773595655096
44.93989387948546
44.83321126482519
44.737592725416576
44.72328261368231
44.46891361472431
44.52454184543361
44.58426682376001
44.51387637071755
44.569100847178746
44.41044347530708
44.54732167727403
44.54058312557369
44.48398498016636
44.51576557569892
44.42062948346581
44.30689015314541
44.2758772069455
44.36946738569843
44.404194750313465
44.32643051593452
44.412608159053825
44.3635916102468
44.569742043413214
44.74756800651288
44.51510284638402
44.4077734001626
44.42228791458091
44.41319009731235
44.23657986174509
44.36465902601845
44.36034199447208
44.33989735029559
44.428609266810966
44.22062340540035
44.51590930028844
44.422998937647904
44.4191173174882
44.36200727785277
44.348682350159045
44.32164259274072
44.02549592554511
43.85768372578342
44.03247414118739
44.157516397634154
44.30909377269607
44.26570360516543
44.37475433345271
44.51840551296919
44.39175609291908
44.39686256009875
44.48585328906516
44.6541522158413
44.539480571537545
44.53400673205559
44.68226770080774
44.81590853381412
44.984892608081466
44.88742672652018
45.22649263153967
45.23345306926748
45.19998308121273
45.093841647361145
45.22660938677856
45.15405908620568
45.277131893665
45.31991915498097
45.26853210801378
45.25120072691356
45.36607197401212
45.41207210755801
45.455901732024174
45.68352709555299
45.689734899912935
45.592097413268455
45.49126424670193
45.55010767181116
45.44675552081348
45.593434993038045
45.55217719704191
45.59978984091193
45.73682526179749
45.61535192212897
45.64010399029286
45.69810989349807
45.661853051796456
45.55135665984468
45.41351654020337
45.63338581696094
45.650244289348876
45.759653107735566
45.72416469530534
45.68822105807317
45.93923312771325
45.77880984668205
45.8904419319333
45.95397505604271
45.84057266870225
45.73242586417506
45.74457149702734
45.68791780910079
45.52211696368338
45.553192019758036
45.66114533595927
45.66572708424421
45.72707848490549
45.40777782643705
45.49018707164968
45.596286891960254
45.70684480701781
45.61022640836443
45.60225285950896
45.73158078655044
45.56324186938386
45.587734927213255
45.6311082721216
45.69839062653282
45.945131603672195
45.63542211191894
45.66119237921773
45.742435454531126
45.650276965534935
45.61960168401218
45.6502608495432
45.63612145876022
45.51159582737886
45.57429773940444
45.49140335858817
45.32436376093304
45.34849429686938
45.09795548067607
45.145907627944716
45.333764174570156
45.455217286593886
45.31218870228476
45.48084171198937
45.459889455419585
45.378360576098636
45.32086013293796
45.39525995076451
45.36631206496898
45.16363400006473
44.85020642249305
44.850085453700856
44.9150544199304
44.964039826885774
44.97714679590409
44.91762760622455
44.9114306434504
44.78906870338383
44.93785052305014
45.067133376459914
45.04229762151795
45.03323033426974
45.04338146686705
45.18800170181416
45.2049224660625
45.00029931382227
44.88082486157969
44.97415561379473
45.17555225466836
45.108611100671226
45.18917059586364
45.25214041413498
45.11666708880903
45.2926344869154
45.237870290951314
45.35995424172902
45.35024589943057
45.30384035442127
45.16579546292753
45.09440535275253
45.117625621022825
44.78607065441137
44.791510328904536
44.85267410017766
45.033655133011486
44.90424216975166
44.751139491620215
45.0515797264036
45.099256774189875
44.873169214526676
44.59173367746157
44.679702493017274
44.80232280952871
44.5198327580638
44.56713577128557
44.578267233362084
44.44089103689408
44.6741916061612
44.65186590502249
44.786580452498065
44.75180450242536
44.681274052116656
44.75966750037614
44.631555244017996
44.48252320001627
44.48711520591073
44.48852276368575
44.64467930032294
44.59359647749494
44.66941435981316
44.557886227474775
44.709859030248516
44.8404325736158
44.79859658707491
44.70148648776024
44.77879270928981
44.91050299017952
44.84484536273794
44.92014407849254
44.999168817966925
45.087846397654566
45.170289541358116
44.9960818283992
45.04893169971431
45.00011209948556
44.85986621736181
44.69402596431239
44.56889427184693
44.62496588750191
44.697197756677625
44.744951263289245
44.73561176610714
44.81203536827589
44.91698010998074
44.587585066877885
44.7566145760915
44.82944564597128
44.97548717250546
44.935705540627154
44.917442991634715
44.98727088364033
44.88779635180172
45.207746529788004
45.21047438975024
45.28362800861588
45.384298345234235
45.20270263883577
45.543954137553975
45.682246379524585
45.538157617331365
45.44598443998348
45.36006617041534
45.314471519612646
45.34038052184767
45.47095397895815
45.32365368979769
45.129448758459525
45.30117295161728
45.23862996669553
45.359639302273266
45.45633747416289
45.494361447179195
45.5076108789418
45.54898456952123
45.71805786599421
45.493580052902516
45.31142472644983
45.569327034323955
45.650096231462946
45.70892194388613
45.557340547055624
45.831109948202396
46.01021516829358
45.845405195713646
45.85629901863015
45.99554496864445
46.13532714437234
45.82321186765322
46.06899103761944
46.088995228082425
46.16844011243776
46.17939132766662
46.15033310266753
46.19864379619386
46.48000334613217
46.51060548766391
46.21518458939578
46.16061293189623
46.084946042597075
45.8484567271826
45.93412406726427
45.95349747773269
45.90865730550228
46.07163762965705
45.87819673938138
45.89768152591927
46.01168136867517
45.72405156636952
45.60803425338316
45.66470581573347
45.64059466771361
45.557961333225464
45.64040558270667
45.80976752233329
45.778641442267215
45.70235235382518
45.74128287741589
45.806698557834146
45.89103170225896
45.717192814290634
45.7073646837368
45.792038942443206
45.7799559296562
45.64941046166228
45.742795752860474
45.804842554806726
45.72110004979768
45.923421787204546
45.99191268307697
46.033853559519955
46.13017298229308
46.12129999870004
46.10015689818685
46.08366022693571
46.18311389977214
46.153096241343924
46.36504662038935
46.26872507026761
46.24922954886846
46.21901438650731
46.09649497310379
46.20437231304897
46.205006044576194
46.16053668406925
45.960976788262755
46.0012458255753
46.17506963261879
45.91128484470169
46.07011243050867
46.1577054592367
46.250629530638896
46.33536331829497
46.15731152044996
46.427812765176625
46.550920082308835
46.25950383689112
46.029559673977936
46.03145413871323
46.02046451874478
45.802304237412265
45.86549190576555
45.912955749762034
45.9096240501054
45.7876234781136
45.5612922382092
45.74442703813263
45.86806057189717
45.63976714929518
45.41321469811324
45.57946491473764
45.68512438846068
45.54567456021499
45.594389229206236
45.827729779346484
45.60126016533618
45.771754649243206
45.762293529444705
45.79529150587843
45.75506544651266
45.78406595386161
45.44868230147096
45.513815961828634
45.477025655425344
45.31734432403478
45.256511140861356
45.50980934907605
45.28686739097197
45.43643423566322
45.39055365727773
45.357139938140755
45.52889780185724
45.397299621104494
45.22274437377528
45.299643495782945
45.41084932050559
45.186935690082066
45.108837194328636
45.14025834122276
45.2253930897866
45.51737015230095
45.46396121033299
45.36236625446966
45.27514067743362
45.246998427717145
45.027305012358035
45.07187210592828
45.0914505208996
44.8953765734529
44.90504838483253
44.875012854504206
44.72303920265815
44.74815447012435
44.83425821406954
44.772951486229005
44.78289840217933
44.84231701722542
44.94941513953168
45.11567465099674
44.91194252511813
44.82038524471248
44.815300048600015
44.89358846769436
44.86018982525871
44.96985936340905
44.755014040066925
45.06349971635146
44.94345469312216
44.90364143760782
44.68631104617165
44.67737059976227
44.960129943348264
45.018858959988876
45.31062261746229
45.38883426707919
45.41496432228635
45.455528980121116
45.436120518018996
45.58027987010922
45.699133361791425
45.68142755332918
45.56555588373788
45.54817355109875
45.610721444018004
45.440246870188815
45.597976448549566
45.76422509332022
45.77722227870103
45.88596527121057
45.640970453023805
45.69899998611406
45.83298375241671
45.75366867349863
45.587445582821076
45.638506217298854
45.73444190672816
45.47610494606933
45.46460183854593
45.47868530760614
45.557242244549904
45.58098880132812
45.55986479196223
45.690023296073264
45.82732097283008
45.750972866518836
45.68665357680944
45.76545161553845
45.75519248843226
45.58282738643238
45.77695707351042
45.846343658071476
45.874801952087616
46.135626908256285
46.028948010794835
46.16939231286306
46.16152173257575
45.93866847353157
45.9616406596279
46.058770981536505
46.059315436056345
45.88478555621318
45.99037551445494
45.92368319811318
45.90138094735314
46.03807102359645
45.94887558436835
46.01560652401691
46.084622059197045
46.250551146602
46.04085242345671
46.039107076501836
45.913466042934346
45.71883555816694
45.801744179790525
45.81908895670216
45.77947586264457
45.889988381235895
45.75642176422385
45.85460973195849
45.78382085687432
45.81243223604708
45.65708324711721
45.58373053264585
45.81650959775638
45.83444696525577
45.96729618577578
46.00082881732134
45.950674507114506
46.031043663064786
46.00595709021797
46.13748221471875
46.22601549859917
45.994124425210586
45.75972969004149
45.60449233672722
45.62980978836675
45.3595158342248
45.25334106834288
45.30320622571777
45.13541085683519
45.338170656445776
45.158019139004274
45.32563308353573
45.52875545732917
45.488270767445634
45.38329281252332
45.34230510064113
45.46936372620057
45.31972503995701
45.28960041283508
45.34630720492122
45.261018841694636
45.29512887627183
45.036684384816795
45.17170478076597
45.09564168371709
45.17645699998118
45.07373668538402
45.082735989924984
45.18055954938631
44.96115661887697
45.06431171075048
45.24367833733388
45.280930793358564
45.345552671955254
45.104575616034396
45.359274060987424
45.45273695942817
45.33176823167369
45.1352202670546
45.23938832627738
45.315829596575604
45.205535625543135
45.27146474179792
45.18254200842475
45.1068250598781
45.197659082815505
45.10274631409749
45.230728019416496
45.317067218977066
45.12728453735801
44.82731941907714
44.782815898091705
44.8392554523459
44.72674085290288
44.74433665532377
44.570839425082795
44.40688832745936
44.38073373651064
44.23455677352206
44.70082346043606
44.80874300526642
44.59159756429275
44.511080817131116
44.72103303431721
44.77380141535627
44.99804025386245
45.05586534828392
45.176764870848814
45.39495008292714
45.33797285546341
45.29055913151336
45.30425332031448
45.42350648565645
45.224783554745684
45.045014634142994
45.1228842247181
45.21329508338879
45.096292491805556
45.293946118889124
45.49471715713885
45.48178576024033
45.575743613044246
45.62098943756548
45.686336109840475
45.71255275163871
45.61938970262273
45.568000668104496
45.497219262171214
45.6412603980304
45.48016361144342
45.53731574600761
45.46785538068846
45.529587551830936
45.552613259230014
45.66921772778592
45.85343914855253
45.55099070454917
45.59925953595052
45.181565095143746
45.240496547728846
44.985361768188504
44.849068092342314
44.828851289557875
44.90702958827895
44.97700845056543
45.2201422168782
44.91806425168146
44.997162825498314
45.16975637515252
44.92708257713122
44.602531356529575
44.51968080796847
44.6002574113583
44.60372992637781
44.65582731547342
44.58329280450943
44.53880439729055
44.603161851916795
44.71110853175489
44.877939475298014
45.104659118364
45.080110595580706
45.056282880450055
45.079950113748126
45.22162823525157
45.10699780687304
45.12424784806054
45.26455970886809
45.110280954069026
45.11135107504415
45.12011718505648
45.19915130362309
45.41085185428603
45.37591919156037
45.030317426801325
44.96820712534066
45.000240749340776
44.852719823672366
44.888182102596545
45.00266305735906
44.842344453377244
44.8931506577189
44.78857007597615
44.84912594433053
45.1845821137924
45.1885694282595
44.96499729112599
44.962295226310204
44.99580256792978
44.87953614266764
44.990470579215874
44.99395685118528
44.87548578406882
44.83384691292874
44.83817491450827
45.05007319275195
44.98800597474294
45.0281166114132
44.79853269763423
44.716185554575056
44.62358432396917
44.43799454007577
44.46170824881085
44.519835492685104
44.41566096705113
44.46725368970129
44.44067257760592
44.770480185739935
44.88534149214217
44.70656930229078
44.59955276762373
44.65575523234152
44.777420170488114
44.644264540596176
44.59751910402001
44.64474774325694
44.44769660023824
44.55948993830869
44.36321966893333
44.36847216308643
44.4415689281425
44.48117893744875
44.30801648232615
44.235838743136306
44.23362054612826
44.116246612078385
44.34163111904154
44.339913734278966
44.17988565571897
44.41726994163124
44.169519259040996
44.20662307000044
44.25078668721027
44.283039718941986
44.125907305420014
44.163259574701605
44.231922253181914
44.18546805991086
44.18496828570008
44.1218773663414
44.29175317583931
44.33612251388216
44.24581707287421
44.34870923721397
44.43110407952073
44.28378143037619
44.06336891540637
44.12484839754243
44.10139485432808
44.01446181808707
44.19071811243979
44.20080187193459
44.25694313830467
44.46075015396652
44.37341996966347
44.676435881257014
44.5600947418582
44.528897095796815
44.47757168766159
44.45174614241379
44.34147203288692
44.167671340520926
44.35838810937355
44.276968485501165
44.24705977686807
44.40016181357398
44.18149268724935
44.126646715735845
44.05309426518501
43.95625244299705
43.96686965008152
44.05182293955066
43.98418735543765
43.777611809753175
43.82246777841895
43.75089673620817
43.58167761734442
43.82693880177184
43.67197840682762
43.910491608200886
44.17507006077202
43.949210559089714
43.76358953015762
43.857467736268624
43.902028446082284
43.667610609321756
43.74221001825464
43.699718501847016
43.55341587709881
43.58421037871615
43.31087761540069
43.60272126785122
43.64918713155103
43.54965717622783
43.29870407557054
43.35757212216038
43.45209013052613
43.631385168638545
43.92540474574685
43.93580534844324
43.97342905195004
44.17572609140527
44.07520385326248
44.29967661579167
44.087398656272825
44.09631676298375
43.934275830476935
43.99604600196378
44.311124819900286
44.23648511032164
44.199204982571345
44.21294993146928
43.93183184952488
44.040426502400166
43.98037741455735
44.00637986709773
44.01624487167338
43.77706847084886
43.56483208498693
43.47357700272143
43.621710809555935
43.45316204391111
43.478872923765536
43.441784944882286
43.46058521361286
43.62001067603192
43.49366250109674
43.551940088498206
43.736330233047156
43.73253812576126
43.58952427045516
43.63471370631826
43.6957231312346
43.648496331767596
43.77881090140585
43.85070583688846
43.85141446769858
43.99772238830562
43.90197938718678
43.94505446057761
43.88648832091449
43.781486584779714
43.605796398104744
43.29738595908224
43.266170323496304
43.17177640308738
43.4285803480317
43.46525824416204
43.34375209081292
43.629612917546915
43.54863038517692
43.62559163188089
43.789746749133485
43.86015841489175
43.733890964196334
43.78156486929042
43.89606256979348
43.808085074592455
43.965320865854984
43.99522988250275
44.04714032097392
43.99441713763518
43.912540189384515
44.251694914790406
44.3125635973745
44.05933105010096
43.99439085335497
44.1608675875632
44.46582730342564
44.31456038881138
44.368155473419534
44.399340729395895
44.41916534898807
44.56027900546952
44.310640616203486
44.32845464790866
44.35493141311242
44.3973657459605
44.26972878118849
44.4464717772961
44.53067037666487
44.405547376517134
44.42303587099818
44.482351796264005
44.27691083501205
44.24654666888733
44.09045968227591
44.1871325370001
44.09039897427153
44.10057744575592
43.96536211377418
44.12671492520618
44.14315779453828
44.01849893039826
44.15038768371073
44.18583814408102
44.13918087666481
43.94027097081811
43.68880800669953
43.878384595535195
44.009573816527485
43.94667871758044
43.88263396470521
43.680813911197966
43.743846204575775
43.59210358160245
43.70791780350811
43.92000749863156
44.10204163284482
44.1831875623588
44.17534613536524
44.388297451180655
44.54254428020773
44.376697017378234
44.432330474042075
44.36272869739915
44.318650540540304
44.25615406768605
44.21315548116567
44.256810817798446
44.234876470395726
44.241302607808464
44.17446960956251
44.10749915269674
43.948586843018134
43.99594202971524
43.89013938738786
43.871222337397995
43.831226413027686
43.64919376097907
43.44058638569318
43.52361497631524
43.5577073147456
43.924047300629994
43.81128612074562
43.98791662707496
44.103854201553425
43.947752031781384
43.89866596665413
43.97875254615707
44.25998125202786
44.00368582497263
43.98897116775191
43.98107619155552
43.752872482311226
43.72664623811424
43.66389282896922
43.65979351438331
43.831324076229535
43.70654958629804
43.537203161681944
43.377702157176
43.58952692122945
43.28374048158491
43.365752936041474
43.2473828338354
43.241533550548155
43.27339526875463
43.42961326300594
43.586846594302
43.655441842246965
43.43648305888151
43.28624383430658
43.39934588273941
43.46537627320112
43.15660220622763
43.20090098791673
43.470209922677796
43.59467021503025
43.830770483575215
43.82281235924941
43.877022922144
44.02508336147242
43.94823947032238
43.803506781867206
43.85025053824003
44.0422961365246
43.9435738337746
43.94752676154764
44.03542767884877
43.97302084425871
44.066882981002735
43.98368573956577
44.150783132718765
44.37761363932165
44.258857592138305
44.058651888790486
44.10908024894071
44.16771213296298
44.01869513082952
44.23419219935844
44.39150667322731
44.41951523357209
44.573383044715634
44.60194970976101
44.789089781629414
44.77576987955459
44.81139515252284
44.70009265743277
44.67190787696193
44.59352559734527
44.428962573134314
44.39875384045614
44.307921583732266
44.45745240069415
44.537177569152796
44.45976225960639
44.57058288396349
44.556972032139115
44.40801126005557
44.3105255058208
44.4426603261301
44.33055176055426
44.218846433026265
44.35623700188151
44.40796771997208
44.32830385027965
44.32980616410108
44.116944252016616
44.152268728561545
44.3525596909643
44.34111466416047
44.12800490385909
44.41359629416099
44.37706247173567
44.356521865675155
44.50419630297432
44.59631612594127
44.57112969695503
44.41810746880653
44.30086403230321
44.57751303467392
44.67989935313371
44.5494674816501
44.42365002591456
44.32647035896202
44.47902264399972
44.184948015966974
44.284863317655116
44.31198422643308
44.31586702630168
44.66490330072842
44.44143504271217
44.73770991618238
44.67055570617359
44.52305823688469
44.62303621355916
44.68838848297238
44.68847428683585
44.6087854321513
44.71841055107777
44.73242171086281
44.707541830674934
44.904627491466165
44.84683548202442
45.03725184059335
45.35148241818159
45.211593418431804
44.90606831076827
44.73976536455269
44.91573746707789
44.946854151822166
45.10260984461751
45.11977201722253
45.08040655905607
45.196404854065676
45.08168003279236
45.26551738570653
45.22145223746722
45.06936194199255
44.85571271836882
44.90560898575335
45.02485103128384
44.785095912663365
44.93881696188907
45.04434557961229
44.95026145309169
45.13412543487732
45.00455542296431
45.32432309140198
45.46849253935127
45.34593340989227
45.269946716427846
45.37537647860102
45.292435406649595
45.2446531348751
45.1422531469438
45.04239725455769
44.804982297399135
44.76272732771328
44.649190350531484
44.89387387339136
44.9102696040959
44.8740631668138
44.63553802053734
44.76055722048136
44.8572249425796
44.752245360362465
44.75620636480323
44.6004446135864
44.788213039561505
45.03006778347371
44.92057992466033
45.070680141442395
44.928288777793355
44.96242471584216
44.82185302995185
44.79834207583319
44.62118026841298
44.42212131071994
44.32178320489355
44.46471036612061
44.45557534563861
44.575286012701
44.46864654065944
44.557309219575515
44.71305560542363
44.58412838136214
44.41198490298046
44.44992769733272
44.454383782514
44.29018002191352
44.36826841412292
44.295726782329346
44.03558253207723
43.97848739359758
43.62403886907679
43.713942143028234
43.77461050551003
43.52200643958796
43.381515168880654
43.22682131484863
42.94872396310214
42.77579997011522
42.969346173771655
43.01529073973313
42.763289022894774
42.7655861129459
42.48742692269661
42.438427318204965
42.35898506060156
42.298147893210256
42.06279375111858
42.170577723667
42.53761431008764
42.49319942341798
42.64900993778313
42.624122287172504
42.48821360027083
42.64063010680123
42.48898057789004
42.56564739664584
42.818143171358656
42.77424273849055
42.731017069445876
42.92007478861125
42.9677147108722
42.788847045925145
42.956486587533085
43.12750815770717
43.02202598142374
43.30454351988112
43.32889386462246
43.44895349539141
43.76639525452806
43.77566981102118
43.72757516198699
43.76554662508362
43.84512716604956
43.680031593290764
43.74147459918524
43.878668519414056
43.952875403631424
44.22585860377072
44.25928919321925
44.55205008208034
44.62499186962366
44.50820767104355
44.36951151848678
44.43669947289799
44.34862419797727
44.14106735702345
44.217337755452796
44.187140995765176
44.227623821967406
44.30272545220528
44.29980286913744
44.260699307852214
44.3948089141483
44.414825470555876
44.18236959219185
44.43730233935145
44.53221282742898
44.513984362168785
44.461593909508856
44.52170642684921
44.646642167459696
44.744010980937254
44.77629772083437
44.85929970741931
44.78381809880469
44.665609671219244
44.49347828266341
44.48701540897924
44.715511385525055
44.50653282631465
44.618246406808865
44.698504693760846
44.70025558205877
44.606100798105984
44.436821926973735
44.616505358345385
44.46841629907826
44.53073665479155
44.3479467022328
44.43135267248459
44.32156509638902
44.065588818781016
44.16211046491498
44.10740849161245
44.06350177337151
44.225967280734054
43.92584080772404
44.11686482807975
44.07339695943722
43.98784180892197
43.70270926243786
43.66717375959529
43.6127200502016
43.5241347217909
43.6586559779833
43.63922958723974
43.68262495994826
43.63089534660251
43.50482278506864
43.64148600504479
43.92334430573757
43.927110772473476
43.59412274054348
43.52576685198624
43.47260716817022
43.30395904487632
43.397896678484386
43.402538834806755
43.410578102162255
43.619385706489844
43.57553280271192
43.62038681422596
43.70632596949818
43.72918465479556
43.783479605822386
43.8240750934276
43.89552503708454
43.68730143791375
43.70840233273557
43.770346034394926
43.78078651273293
43.964936170694294
43.84754518191316
44.02948504894988
44.222484852015235
44.23854023247108
44.03468673919064
44.023053642802495
43.95881223504089
43.84758055983364
43.89406006916184
44.00433405173729
44.0488771575978
44.090307735007265
44.137096027097996
44.344742580907564
44.39039836434515
44.228105142167784
43.983841280505104
43.79360818713633
43.94601866035823
43.74622492293162
43.76695729633747
43.74222126776034
43.615690232165186
43.793871246024345
43.642781177158014
43.77340485912816
43.923826298950125
43.98811628977674
43.94171855125214
44.046858778589744
44.102553246676074
44.04011493001804
44.00816391590779
44.09432102989028
44.01804103194742
44.09425219222292
43.856672296152674
43.97776439381089
44.200952508561
44.41010466694708
44.274685467232246
44.33491681721571
44.19649205846932
44.067668074512284
44.10582077471155
44.11326795319359
44.14982796375646
44.28325671304477
44.28651607261046
44.45051620413542
44.61405428373949
44.60389185999934
44.559537857325175
44.6834653965921
44.6950566088204
44.47044239179465
44.624893138987666
44.55597836582434
44.54595475921776
44.75749559765588
44.51322061985562
44.55734379381946
44.563311409914384
44.40920419806519
44.422672013622844
44.3921815725231
44.24987730909045
43.96053113223252
43.90404502046357
43.95327490085023
43.95494259904494
43.88604014446881
43.82201574616997
43.94915277523521
43.85748901344594
43.84088604602994
43.84315960408065
43.93376474117996
43.921555410128086
43.737538181618746
43.69989874999762
43.92293641455671
43.84626147210702
43.79606727666459
43.46972978192978
43.327636922799904
43.416789765589414
43.32907209773773
43.097941794408506
43.162267571996466
43.23572757568811
43.24623607308534
43.42594504733363
43.398460537728305
43.287126763764526
43.23863092198998
43.017013744336964
43.25418543703617
43.29868532109166
43.2701338399269
43.133525632593866
43.034503044547364
42.95037507984589
42.84760216048783
42.73988319048336
42.71442373270476
42.48812316609837
42.644308627757894
42.603635220358946
42.8349921419304
43.039364454990825
43.25122069793104
42.87733900976853
42.864958557343726
43.118096139276254
43.209708643410856
43.28466396379052
43.451817485694164
43.283464603409115
43.36935933512218
43.29111615993964
43.4362152786303
43.45394166627572
43.592311043177226
43.54597728188568
43.59185237307499
43.54178969915017
43.253428761464335
43.40216946654778
43.459512963393536
43.29977515325436
43.25474411379145
43.32812090289989
43.48546383164459
43.646829335105686
43.618906389521115
43.64691223196256
43.54427520558964
43.576181916759914
43.36517673312593
43.56366092050217
43.59740334827565
43.54522762625392
43.71795702330216
43.59988697764499
43.732975661658955
43.827385055498034
43.78541171675632
43.55209678658859
43.684541870448165
43.71601666929217
43.693024135654916
43.66444722031846
43.75503730835946
43.68367797757598
43.96562986834564
43.96703502689302
44.16454717388864
44.24705150173105
43.896087850472085
43.49619652852339
43.464584326776915
43.389684215825525
43.30097994678336
43.34654668989021
43.236752673927654
43.24751315466082
43.30152985862434
43.09187354240026
43.349570516884235
43.538966057450466
43.27732273461453
42.97770722553955
43.30409112401302
43.17395832663016
43.009799741372866
43.124454849013574
42.95340278753539
42.72083231077532
42.727998296721566
42.68401832749416
42.807026535997906
42.820621318231844
42.982078960941365
43.024014312770674
43.05588068706835
43.1349061521843
43.08910892131807
43.07024204689391
42.82359000321495
42.76275917114535
43.02898921624051
43.15349654883685
43.22024253314711
43.34640472717287
43.308232234466665
43.16363759054799
43.207218635673776
43.29159824505307
43.22360872194648
43.1357590019526
43.035319587617956
43.14917295691046
43.44529028408657
43.44864777906704
43.460177523051634
43.660113739100986
43.712776187332764
43.62936919914637
43.6092134679631
43.51152115639617
43.34273274348118
43.294641787354976
42.974523188568256
43.11441092061891
43.25432233191711
43.10262040267729
43.20160167936173
43.304645115982666
43.474583301473935
43.34398868304718
43.42941632915171
43.57634635297704
43.48799305519335
43.4027290789775
43.33246929147878
43.233405520430615
43.043716022056415
42.93103634712443
43.1145689234349
43.0858475925002
43.06255989039057
43.26138451470339
42.93371515680045
42.712219979243656
42.76955281008622
42.83465280651022
42.82427359021459
42.777897970419204
42.978936922277164
42.785564560663865
42.917380062759875
42.89036781800537
42.607243461779845
42.59045636061046
42.71580830669322
42.82142415423598
42.72062792309052
42.802956615087766
42.8490892791677
42.90207102103667
42.959537257813395
42.90665917640421
43.18189545925967
43.36699763015742
43.378541716389904
43.278179658335375
43.409241688885274
43.46132719716446
43.27121430664963
43.36598790031892
43.44345767381059
43.259516031562974
43.388932770528
43.108588227173676
43.28001836524386
43.35562663474872
43.331781753952406
43.08989578173635
43.21494842483765
43.19559431421374
43.1285989585513
43.13159684120932
43.21437568817234
43.23952032320996
43.24932255289023
43.206935611825216
43.477675018597516
43.582488977446
43.49184466214392
43.42742449210497
43.33708593353731
43.31389852704221
43.343311081117704
43.28445677952324
43.402428445247914
43.33461049473203
43.52563779284917
43.56698703833392
43.86952471801723
43.85634260445782
43.822581960959305
43.735503654862065
43.97720752710286
44.22520937820862
44.064616955959025
44.43871864879806
44.579357136247665
44.57518752298516
44.63233079371643
44.60482015144782
44.84380172658411
44.75881199844361
44.577069281479616
44.31671398445433
44.34632182812577
44.46923231041871
44.265247346041775
44.31466597296876
44.29330712514871
44.14720225349861
44.1736375133493
44.21668506527781
44.36577901993093
44.50254484173141
44.53390885175439
44.43787460430653
44.515303422510684
44.57227828531713
44.49421025589427
44.692727662046835
44.717602845853094
44.76201001223902
45.06379756660235
45.08013490101387
45.19858774430164
45.18100070906657
45.15410661066787
44.87930175353439
44.88980882548035
44.74451024710485
44.66111313221029
44.7023038973988
44.84354817471294
44.91991308759083
45.024684777720196
44.95216117452416
44.988403186345984
45.34326694336331
45.37204192489825
45.26746275358537
45.223301176197445
45.3217913780317
45.21119904250781
45.403513608236985
45.48379662173289
45.40845598332913
45.43435061721683
45.254609885561784
45.28436212200014
45.269744063853366
45.24671188913596
45.071567722241376
45.067446396139125
45.0035503484722
44.68639649985738
44.75697385323429
44.75840310757301
44.76778328837826
44.85511596816258
44.82019912159627
44.89094996815639
45.00807299794216
44.77529048430778
44.63718525378267
44.69199076051318
44.830516449878
44.63972870886601
44.649321646234625
44.79744270219027
44.75687941079557
44.7978903390689
44.580468036479495
44.53747385332668
44.60911476733906
44.4118019096648
44.24743405391471
44.302045495072214
44.20490352175748
44.274281666028216
44.22878947470566
44.37512406114794
44.21825278130487
44.21101555142755
44.17564817861093
44.38942651812936
44.214065903887764
43.959004532588416
43.97875244360636
43.927381681642096
44.09025524548064
44.003178710246644
44.130896256674305
44.201827031752885
44.029922114154346
44.11105014364506
44.028514892886136
44.19178421863668
44.36809887721828
44.14481092365196
44.06964233899311
43.918926380475
43.99894054645519
43.86351408756736
44.0406869517933
44.1543224438588
44.18043419732441
44.34099209042665
44.30282731743429
44.49176100191269
44.368264002510884
44.32179682476001
43.992940665693524
44.12024592160342
44.13241448209135
43.93284597808629
44.00486504340702
44.09678918110362
43.82547765428308
43.746949864602605
43.59171434060608
43.670124928671186
43.65356220134159
43.759388421859136
43.21662294328996
43.311220086726905
43.43828984176962
43.3721595460138
43.64074594559412
43.6341182101752
43.55285662437472
43.80546128458102
43.69858160581945
43.84801184205333
43.91453602692752
43.82720097458298
43.68254553346156
43.650705647956094
43.79221735820877
43.55890050818399
43.641339651500786
43.848524896798615
43.8180336734515
43.92218229292494
43.895859520993284
44.13126711631021
44.29348598008995
44.23672588867278
44.154754763143465
44.26526230165727
44.391547489116256
44.09716053526548
44.038376957395236
43.96923402796102
43.853365404359145
43.93589551203212
43.93525122502303
44.029027718763395
44.119543910706284
44.00623751168981
43.98747092104702
43.92844979123119
44.01449904369
43.957303886014856
44.08979775115124
44.08296314160015
43.95124814552815
43.907766914755925
43.90424940039463
44.15175754828221
44.123871361828044
44.237798230388655
43.927127068911425
43.84194095173954
43.9639322500347
43.82415783173205
43.8270761031638
43.94715910623893
44.059207297522576
44.10747985331972
43.91610969891481
44.06929712840907
44.01468697000688
43.86116855765265
43.528184032233625
43.566494195348476
43.61603749173328
43.50405995077831
43.54551251147654
43.48024189119754
43.384429569363775
43.48445201283564
43.37385861551627
43.58547037350152
43.5875953087815
43.45828876434309
43.28070545117425
43.12215983796682
43.0538468166313
42.92986127959927
42.90137992150602
42.81815931616647
42.82176647459319
43.00470249608008
42.75978015840387
42.88247470387039
42.843558309964195
42.78569047730736
42.69908748824082'''


@app.get("/all_algos")
async def algos_list():
    return algos.get_all_algos_names()


@app.get("/get_algo_params")
async def get_algo_params(algo: str):
    return algos.get_algo_params(algo)


@app.get("/execute_algo")
async def execute_algo(request: Request):
    # algo = request.query_params["algo"]
    # kwargs = {k: v for k, v in request.query_params.items() if k in algos.get_algo_params(algo)}
    # return await algos.execute_algo(algo, **kwargs)
    return [float(el) for el in a.split("\n")]