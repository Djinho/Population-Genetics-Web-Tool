--
-- File generated with SQLiteStudio v3.4.4 on Wed Feb 14 21:56:51 2024
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: admixture_results
CREATE TABLE IF NOT EXISTS admixture_results (
    ResultID INTEGER PRIMARY KEY AUTOINCREMENT,
    PopulationID INTEGER,
    ancestry_1 REAL,
    ancestry_2 REAL,
    ancestry_3 REAL,
    ancestry_4 REAL,
    ancestry_5 REAL,
    FOREIGN KEY (PopulationID) REFERENCES populations(PopulationID)
);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (1, 6, 0.0819545, 0.01784979310345, 0.88686725, 0.00671289655172, 0.00661560344828);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (2, 7, 0.18576812162162, 0.02669624324324, 0.74001571621622, 0.0384357972973, 0.00908416216216);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (3, 8, 0.59195409923664, 0.00008504580153, 0.00396786259542, 0.01193072519084, 0.39206226717557);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (4, 9, 0.00455674193548, 0.00024204301075, 0.00040396774194, 0.00981174193548, 0.98498547311828);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (5, 10, 0.93107532402235, 0.00195579329609, 0.00133110055866, 0.05455217877095, 0.01108558659218);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (6, 11, 0.00509421359223, 0.0002466407767, 0.00048533009709, 0.03543294174757, 0.95874085436893);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (7, 12, 0.00200298773006, 0.0002562392638, 0.00022486503067, 0.02073638650307, 0.97677951533742);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (8, 13, 0.5951738030303, 0.00494636363636, 0.0681876969697, 0.31331975, 0.0183725);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (9, 14, 0.00064367114094, 0.00039308053691, 0.99741105369128, 0.00075239597315, 0.00079980536913);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (10, 15, 0.83541337373737, 0.04454068686869, 0.00016625252525, 0.0837995959596, 0.03608005050505);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (11, 16, 0.93856657142857, 0.00065334065934, 0.00073296703297, 0.0532067032967, 0.00684038461538);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (12, 17, 0.69540110679612, 0.0001765631068, 0.00345640776699, 0.00731939805825, 0.29364650485437);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (13, 18, 0.01240256741573, 0.00423142696629, 0.97989024157303, 0.0019200505618, 0.00155573033708);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (14, 19, 0.93358200636943, 0.0037408343949, 0.01202501273885, 0.04019887261146, 0.01045328025478);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (15, 20, 0.64387841121495, 0.00033288785047, 0.00657041121495, 0.00547104672897, 0.34374725233645);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (16, 21, 0.00278125961538, 0.00010518269231, 0.00019842307692, 0.06243959615385, 0.93447551923077);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (17, 22, 0.01393551639344, 0.00066687704918, 0.00076954098361, 0.01206863934426, 0.97255940163934);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (18, 23, 0.02897002020202, 0.00608894949495, 0.95127935353535, 0.00418726262626, 0.00947437373737);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (19, 24, 0.00136722222222, 0.00203594949495, 0.99405211111111, 0.00162448484848, 0.00092025252525);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (20, 25, 0.45199095876289, 0.00307613402062, 0.04105631958763, 0.466705, 0.03717151546392);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (21, 26, 0.17694051639344, 0.00178690163934, 0.02755229508197, 0.78077604098361, 0.0129442704918);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (22, 27, 0.70520401369863, 0.00013688356164, 0.00455182876712, 0.01083366438356, 0.27927364383562);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (23, 28, 0.65330849640288, 0.01033510791367, 0.14254738129496, 0.17719958992806, 0.01660939568345);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (24, 29, 0.00003325344353, 0.97412366528926, 0.00098533746556, 0.00607786088154, 0.01877988429752);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (25, 30, 0.63311384210526, 0.00013030701754, 0.00979011403509, 0.00359949122807, 0.35336624561404);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (26, 31, 0.94064026168224, 0.0012928411215, 0.0044983364486, 0.04128296261682, 0.01228557943925);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (27, 32, 0.00067157303371, 0.00070933707865, 0.99686247191011, 0.00085440449438, 0.00090224157303);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (28, 1, 0.03211652183651, 0.00648206942889, 0.95263360470325, 0.0053799193729, 0.00338790145577);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (29, 2, 0.47918916122449, 0.00531813673469, 0.0737932755102, 0.42145716734694, 0.02024227346939);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (30, 3, 0.00250838596491, 0.53958486651411, 0.00072775438596, 0.01550017925248, 0.44167880625477);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (31, 4, 0.91483780837004, 0.01144190969163, 0.00540177973568, 0.05256931718062, 0.01574916740088);
INSERT INTO admixture_results (ResultID, PopulationID, ancestry_1, ancestry_2, ancestry_3, ancestry_4, ancestry_5) VALUES (32, 5, 0.67160865531915, 0.00018860638298, 0.00604188085106, 0.00708799361702, 0.31507287234043);

-- Table: pca_coordinates
CREATE TABLE IF NOT EXISTS pca_coordinates (
    CoordinateID INTEGER PRIMARY KEY AUTOINCREMENT,
    PopulationID INTEGER,
    pc1 REAL,
    pc2 REAL,
    pc3 REAL,
    pc4 REAL,
    pc5 REAL,
    pc6 REAL,
    pc7 REAL,
    pc8 REAL,
    pc9 REAL,
    pc10 REAL,
    FOREIGN KEY (PopulationID) REFERENCES populations(PopulationID)
);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (1, 6, -0.01707765948276, 0.01504398094828, -0.00166858108974, 0.00248258494241, 0.00516169928448, 0.00638879937931, -0.00224888069536, -0.00051600775862, -0.00022263665517, 0.01078057028448);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (2, 7, -0.01290070189189, 0.01243956895946, -0.00220527372973, 0.00557573037838, 0.00696743432432, 0.00599929287838, -0.00208293436487, 0.00028036331081, -0.00096857612838, 0.00425168360811);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (3, 8, 0.0015402116116, -0.01230229083969, -0.03213816335878, -0.00633567175573, -0.00722429057252, -0.00116747279695, -0.00073091377557, -0.00055648880916, -0.00028841202672, 0.00199912093634);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (4, 9, -0.00500200150538, -0.03007169139785, 0.00603170817204, -0.00528019065591, 0.01792153548387, 0.00094521383118, 0.00201514906989, 0.00111385780645, -0.00051596644516, 0.00070332852043);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (5, 10, 0.01081907268156, 0.00345041067039, -0.00781794441341, 0.00860474290503, 0.02463296424581, 0.00024448302704, -0.00065889576464, 0.00282596849771, -0.00372613228492, 0.00284025986313);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (6, 11, -0.00463172058252, -0.02961102135922, 0.00785491058252, -0.00197699271845, 0.01376289213592, 0.00010068948641, -0.00072275930874, 0.00097778528573, -0.00219326916893, 0.00046725109903);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (7, 12, -0.00496962705522, -0.03055283128834, 0.00865214042945, -0.0039884260092, 0.01726131288344, 0.00034630822393, 0.0002065775184, 0.0026934755681, -0.00212046668896, 0.00028808597669);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (8, 13, 0.00469819113046, -0.00325448489167, -0.00535704234848, 0.02787545454546, 0.00820948336364, 0.00134319460951, 0.00056624290909, -0.00054892575, 0.00257282979394, -0.00352541192273);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (9, 14, -0.02051181073826, 0.01635648993289, -0.00154505455906, 0.00189686033624, 0.00266388910268, 0.01971582892617, -0.00669507855638, -0.00126898350268, 0.00022996592081, 0.02079112825503);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (10, 15, 0.01073281565657, 0.0021382684498, -0.00375021834343, 0.00824934454545, 0.01891304343434, -0.00109036354858, -0.00293198435354, 0.00568713991616, -0.00560442992828, 0.00711873717172);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (11, 16, 0.01096007340659, 0.00350424153846, -0.00766988791209, 0.00834956351648, 0.02327682307692, 0.00043737754945, 0.0000956013044, 0.00083882187912, -0.00141040595604, 0.00199059950769);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (12, 17, 0.00315276427184, -0.00901509019418, -0.03453246213592, -0.0061099528835, -0.0078061141068, -0.00093314933553, -0.00042788191068, 0.00081011681748, 0.00030072669418, 0.00040850756039);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (13, 18, -0.01973179550562, 0.01600178651685, -0.0017862840764, 0.00307815133371, 0.00521874744382, -0.04540795168539, 0.02008561578652, 0.00653746528652, 0.00021809984607, -0.02049705769663);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (14, 19, 0.0099671210828, 0.0036037133758, -0.00925634248408, 0.00953012394905, 0.02735379872612, 0.00047528671592, -0.00034455592994, 0.0011694062293, -0.00003612259554, -0.00256771490064);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (15, 20, 0.00191646849626, -0.01072780130841, -0.03672267570094, -0.00749183654206, -0.00960852158878, -0.00126411056899, -0.00049012057196, 0.00073461985047, -0.00068297306075, -0.00089898251589);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (16, 21, -0.00453115442308, -0.02941949903846, 0.00748848115385, -0.0003483560625, 0.01075128115385, -0.00042943096231, -0.00214978123077, -0.00048107242692, -0.00128553058654, 0.00064274805596);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (17, 22, -0.00477782139344, -0.02966888196721, 0.00573608204918, -0.00545173327049, 0.01728914016393, 0.00090128595246, 0.00261799865738, 0.00086882113607, -0.00071341581147, -0.00022861207246);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (18, 23, -0.01890212626263, 0.01489065151515, -0.00297643387879, 0.00173447024515, 0.00363905883838, 0.0421547, -0.03145511111111, -0.00560535141313, -0.00565352056667, -0.04697193737374);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (19, 24, -0.02053575252525, 0.01693561818182, -0.00014337866636, 0.00139218781313, 0.00177711523939, -0.02535401818182, 0.01176952580808, 0.00122232479646, 0.00093141604343, -0.00039646289899);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (20, 25, 0.0034653002, -0.00807605291753, -0.0034848841433, 0.03798879793814, -0.00282038549072, -0.00041109314845, -0.0007055660701, -0.00066710168041, 0.0035282835433, -0.0005807589268);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (21, 26, 0.00060920686229, -0.01552081959016, 0.00005187444639, 0.05970427459016, -0.02438891952459, 0.00050297288852, -0.0000622322, -0.00174190759344, 0.00349036363853, 0.00064660277869);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (22, 27, 0.00346783962329, -0.00835042732877, -0.03308096643836, -0.00588488558904, -0.00570415267945, -0.00138711061849, -0.00137697424589, -0.00144917490479, 0.00051586109178, 0.00171949959041);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (23, 28, 0.00396557639554, 0.00117587185252, -0.00726497755396, 0.01911235906475, 0.01545590594245, 0.00075235747191, 0.00016741193381, -0.00327452847842, 0.00151866367266, -0.0042819439);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (24, 29, 0.02790242286501, 0.00831523373025, 0.00589730497576, -0.00328440905908, -0.00381407793314, -0.00018009245331, -0.00014913118953, -0.00042595506639, 0.00002883566928, -0.0002921130573);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (25, 30, 0.00167799201754, -0.01090004552632, -0.03717118508772, -0.00774736596491, -0.0095891627193, -0.0002750588886, 0.0009555449114, 0.00158930647456, 0.00054882371491, 0.00006637896053);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (26, 31, 0.00989212065421, 0.00313777514019, -0.01099540476636, 0.00826508495327, 0.02397798598131, 0.00142068928598, 0.00010691986916, 0.00094073970178, -0.00070930846168, -0.004702638);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (27, 32, -0.02048440786517, 0.01629264775281, -0.00158835151421, 0.00225891069545, 0.0032810747809, 0.0141982391573, -0.00378954290225, -0.00134469448708, 0.0010014647191, 0.01933738353933);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (28, 1, -0.01909826924972, 0.01567968297089, -0.00167581788221, 0.00251148071711, 0.00398705075364, 0.00025828172564, -0.00051595294531, 0.00029362263197, -0.00035122219317, -0.00026074443113);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (29, 2, 0.00322823205061, -0.00600625090041, -0.00418095214171, 0.03531635267347, -0.00003469968286, 0.00061911435521, 0.00004486139918, -0.00164252907531, 0.00269137887939, -0.00211835235265);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (30, 3, 0.01331100088482, -0.00874834920812, 0.00651437910175, -0.00337957504721, 0.00484840766632, 0.00006809541489, 0.00010235403112, 0.00029752741879, -0.0006249617759, -0.00000962969094);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (31, 4, 0.01031544129956, 0.00315440417738, -0.00814754514537, 0.00871605493392, 0.02390038127753, 0.00034909500813, -0.00071414446542, 0.00203439552597, -0.00168447744009, -0.00004496469207);
INSERT INTO pca_coordinates (CoordinateID, PopulationID, pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10) VALUES (32, 5, 0.00261147345553, -0.00965573746809, -0.03522022574468, -0.0067517971766, -0.00799598383872, -0.00098989165115, -0.00040132097447, 0.00028010161319, 0.00020378373383, 0.00043510487494);

-- Table: populations
CREATE TABLE IF NOT EXISTS populations (
    PopulationID INTEGER PRIMARY KEY AUTOINCREMENT,
    PopulationName TEXT NOT NULL,
    is_Superpopulation INTEGER NOT NULL CHECK (is_Superpopulation IN (0,1))
);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (1, 'AFR', 1);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (2, 'AMR', 1);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (3, 'EAS', 1);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (4, 'EUR', 1);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (5, 'SAS', 1);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (6, 'ACB', 0);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (7, 'ASW', 0);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (8, 'BEB', 0);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (9, 'CDX', 0);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (10, 'CEU', 0);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (11, 'CHB', 0);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (12, 'CHS', 0);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (13, 'CLM', 0);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (14, 'ESN', 0);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (15, 'FIN', 0);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (16, 'GBR', 0);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (17, 'GIH', 0);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (18, 'GWD', 0);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (19, 'IBS', 0);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (20, 'ITU', 0);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (21, 'JPT', 0);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (22, 'KHV', 0);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (23, 'LWK', 0);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (24, 'MSL', 0);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (25, 'MXL', 0);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (26, 'PEL', 0);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (27, 'PJL', 0);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (28, 'PUR', 0);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (29, 'SIB', 0);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (30, 'STU', 0);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (31, 'TSI', 0);
INSERT INTO populations (PopulationID, PopulationName, is_Superpopulation) VALUES (32, 'YRI', 0);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
