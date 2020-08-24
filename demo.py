# # import csv
# # from reportlab.lib import colors
# # from reportlab.lib.pagesizes import A4, inch,mm,landscape,LETTER
# # from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table
# #
# # with open('../PREETI AGGARWAL.csv', '+r') as f:
# #     data = csv.reader(f)
# #     d = []
# #     for row in data:
# #         d.append(row)
# #
# # print(d)
# # doc = SimpleDocTemplate("complex_cell_values3.pdf")
# # # container for the 'Flowable' objects
# # elements = []
# # t = Table(data=d, style=[
# #     ('BOX', (0, 0), (-1, -1), 1, colors.black),
# #     ('GRID', (0, 0), (-1, -1), 0.5, colors.black),('SIZE',(0,0),(-1,-1),5.5)],colWidths=0.9*inch)
# # # t._argW[8] = 0.01 * mm
# # # print(t)
# #
# # elements.append(t)
# # # write the document to disk
# # doc.build(elements)
#
#
# # import requests
# #
# # headers = {
# #     'Authorization': 'Token 1d4402515c3b5b6a3537ad413cda8e5a8919e897',
# #     'Content-Type': 'application/json; charset=utf-8'
# # }
# # r = requests.get(url='http://127.0.0.1:8000/Shopping/ShoppingAPI/list',headers=headers)
# # files = r.json()
# # print(files)
#
# # from database import *
# from random import choice, randint, randrange
# import os
# from PIL import Image
# import datetime
# import time
# # import pandas as pd
# # import database
# import sqlite3
#
# image = ['228.jpg', '552.jpg', '584.jpg', '609.jpg', '475.jpg', '62.jpg', '385.jpg', '549.jpg', '144.jpg', '570.jpg',
#          '470.jpg', '216.jpg', '219.jpg', '9.jpg', '243.jpg', '133.jpg', '36.jpg', '212.jpg', '29.jpg', '533.jpg',
#          '453.jpg', '652.jpg', '746.jpg', '231.jpg', '333.jpg', '434.jpg', '719.jpg', '716.jpg', '732.jpg', '321.jpg',
#          '23.jpg', '656.jpg', '107.jpg', '314.jpg', '480.jpg', '668.jpg', '474.jpg', '447.jpg', '164.jpg', '722.jpg',
#          '424.jpg', '302.jpg', '364.jpg', '681.jpg', '60.jpg', '663.jpg', '624.jpg', '688.jpg', '405.jpg', '230.jpg',
#          '573.jpg', '281.jpg', '497.jpg', '47.jpg', '296.jpg', '353.jpg', '761.jpg', '591.jpg', '58.jpg', '510.jpg',
#          '330.jpg', '548.jpg', '105.jpg', '69.jpg', '82.jpg', '420.jpg', '273.jpg', '61.jpg', '211.jpg', '188.jpg',
#          '686.jpg', '50.jpg', '690.jpg', '575.jpg', '378.jpg', '269.jpg', '276.jpg', '729.jpg', '14.jpg', '87.jpg',
#          '264.jpg', '425.jpg', '143.jpg', '66.jpg', '558.jpg', '347.jpg', '217.jpg', '443.jpg', '64.jpg', '626.jpg',
#          '309.jpg', '692.jpg', '666.jpg', '600.jpg', '237.jpg', '286.jpg', '253.jpg', '342.jpg', '542.jpg', '99.jpg',
#          '608.jpg', '648.jpg', '764.jpg', '376.jpg', '738.jpg', '702.jpg', '262.jpg', '694.jpg', '4.jpg', '363.jpg',
#          '554.jpg', '416.jpg', '505.jpg', '186.jpg', '95.jpg', '731.jpg', '92.jpg', '646.jpg', '81.jpg', '632.jpg',
#          '720.jpg', '612.jpg', '19.jpg', '141.jpg', '718.jpg', '387.jpg', '444.jpg', '726.jpg', '593.jpg', '328.jpg',
#          '300.jpg', '539.jpg', '551.jpg', '487.jpg', '513.jpg', '122.jpg', '707.jpg', '245.jpg', '180.jpg', '57.jpg',
#          '521.jpg', '222.jpg', '388.jpg', '326.jpg', '471.jpg', '202.jpg', '346.jpg', '209.jpg', '115.jpg', '18.jpg',
#          '586.jpg', '11.jpg', '685.jpg', '700.jpg', '623.jpg', '743.jpg', '620.jpg', '514.jpg', '605.jpg', '495.jpg',
#          '675.jpg', '582.jpg', '386.jpg', '56.jpg', '490.jpg', '756.jpg', '84.jpg', '173.jpg', '525.jpg', '445.jpg',
#          '345.jpg', '460.jpg', '168.jpg', '714.jpg', '320.jpg', '97.jpg', '461.jpg', '574.jpg', '742.jpg', '602.jpg',
#          '35.jpg', '22.jpg', '83.jpg', '272.jpg', '249.jpg', '699.jpg', '120.jpg', '687.jpg', '121.jpg', '496.jpg',
#          '93.jpg', '338.jpg', '160.jpg', '203.jpg', '151.jpg', '360.jpg', '530.jpg', '233.jpg', '441.jpg', '736.jpg',
#          '760.jpg', '594.jpg', '131.jpg', '158.jpg', '247.jpg', '509.jpg', '294.jpg', '371.jpg', '59.jpg', '499.jpg',
#          '408.jpg', '127.jpg', '31.jpg', '372.jpg', '223.jpg', '331.jpg', '196.jpg', '644.jpg', '446.jpg', '25.jpg',
#          '68.jpg', '282.jpg', '369.jpg', '751.jpg', '596.jpg', '481.jpg', '88.jpg', '44.jpg', '491.jpg', '438.jpg',
#          '483.jpg', '547.jpg', '165.jpg', '252.jpg', '246.jpg', '493.jpg', '157.jpg', '683.jpg', '538.jpg', '65.jpg',
#          '585.jpg', '740.jpg', '555.jpg', '682.jpg', '227.jpg', '98.jpg', '730.jpg', '241.jpg', '116.jpg', '89.jpg',
#          '350.jpg', '660.jpg', '270.jpg', '578.jpg', '373.jpg', '529.jpg', '150.jpg', '625.jpg', '432.jpg', '146.jpg',
#          '117.jpg', '291.jpg', '741.jpg', '256.jpg', '204.jpg', '76.jpg', '317.jpg', '524.jpg', '140.jpg', '661.jpg',
#          '462.jpg', '734.jpg', '611.jpg', '592.jpg', '455.jpg', '765.jpg', '48.jpg', '724.jpg', '590.jpg', '176.jpg',
#          '482.jpg', '106.jpg', '248.jpg', '419.jpg', '210.jpg', '745.jpg', '401.jpg', '394.jpg', '78.jpg', '358.jpg',
#          '236.jpg', '744.jpg', '134.jpg', '535.jpg', '101.jpg', '70.jpg', '606.jpg', '278.jpg', '422.jpg', '384.jpg',
#          '283.jpg', '421.jpg', '754.jpg', '672.jpg', '265.jpg', '175.jpg', '489.jpg', '267.jpg', '627.jpg', '289.jpg',
#          '409.jpg', '673.jpg', '319.jpg', '679.jpg', '229.jpg', '645.jpg', '435.jpg', '75.jpg', '654.jpg', '224.jpg',
#          '705.jpg', '502.jpg', '311.jpg', '403.jpg', '55.jpg', '135.jpg', '397.jpg', '759.jpg', '295.jpg', '185.jpg',
#          '566.jpg', '28.jpg', '41.jpg', '484.jpg', '375.jpg', '103.jpg', '341.jpg', '577.jpg', '361.jpg', '749.jpg',
#          '348.jpg', '355.jpg', '512.jpg', '80.jpg', '477.jpg', '100.jpg', '172.jpg', '486.jpg', '520.jpg', '406.jpg',
#          '238.jpg', '671.jpg', '750.jpg', '111.jpg', '629.jpg', '523.jpg', '197.jpg', '537.jpg', '562.jpg', '114.jpg',
#          '684.jpg', '541.jpg', '288.jpg', '665.jpg', '395.jpg', '337.jpg', '468.jpg', '437.jpg', '359.jpg', '698.jpg',
#          '191.jpg', '15.jpg', '183.jpg', '138.jpg', '515.jpg', '292.jpg', '74.jpg', '567.jpg', '153.jpg', '735.jpg',
#          '503.jpg', '340.jpg', '336.jpg', '380.jpg', '193.jpg', '192.jpg', '37.jpg', '298.jpg', '680.jpg', '119.jpg',
#          '205.jpg', '244.jpg', '51.jpg', '436.jpg', '703.jpg', '442.jpg', '500.jpg', '152.jpg', '619.jpg', '163.jpg',
#          '170.jpg', '704.jpg', '182.jpg', '522.jpg', '254.jpg', '5.jpg', '124.jpg', '727.jpg', '429.jpg', '334.jpg',
#          '1.jpg', '669.jpg', '177.jpg', '316.jpg', '377.jpg', '440.jpg', '451.jpg', '392.jpg', '488.jpg', '506.jpg',
#          '532.jpg', '417.jpg', '428.jpg', '536.jpg', '271.jpg', '184.jpg', '588.jpg', '315.jpg', '33.jpg', '696.jpg',
#          '261.jpg', '402.jpg', '39.jpg', '599.jpg', '601.jpg', '641.jpg', '650.jpg', '559.jpg', '208.jpg', '762.jpg',
#          '194.jpg', '136.jpg', '356.jpg', '518.jpg', '260.jpg', '91.jpg', '335.jpg', '280.jpg', '46.jpg', '86.jpg',
#          '10.jpg', '431.jpg', '332.jpg', '640.jpg', '318.jpg', '713.jpg', '279.jpg', '301.jpg', '275.jpg', '206.jpg',
#          '284.jpg', '617.jpg', '712.jpg', '399.jpg', '38.jpg', '108.jpg', '142.jpg', '169.jpg', '469.jpg', '676.jpg',
#          '485.jpg', '563.jpg', '517.jpg', '576.jpg', '263.jpg', '259.jpg', '411.jpg', '235.jpg', '104.jpg', '72.jpg',
#          '693.jpg', '657.jpg', '129.jpg', '614.jpg', '17.jpg', '6.jpg', '653.jpg', '13.jpg', '155.jpg', '32.jpg',
#          '322.jpg', '717.jpg', '325.jpg', '125.jpg', '546.jpg', '166.jpg', '67.jpg', '610.jpg', '427.jpg', '368.jpg',
#          '324.jpg', '226.jpg', '728.jpg', '492.jpg', '71.jpg', '323.jpg', '251.jpg', '305.jpg', '268.jpg', '658.jpg',
#          '132.jpg', '553.jpg', '147.jpg', '201.jpg', '85.jpg', '414.jpg', '508.jpg', '306.jpg', '94.jpg', '198.jpg',
#          '412.jpg', '664.jpg', '250.jpg', '365.jpg', '362.jpg', '659.jpg', '695.jpg', '564.jpg', '242.jpg', '534.jpg',
#          '52.jpg', '448.jpg', '572.jpg', '12.jpg', '381.jpg', '649.jpg', '479.jpg', '433.jpg', '670.jpg', '344.jpg',
#          '708.jpg', '628.jpg', '439.jpg', '526.jpg', '747.jpg', '456.jpg', '112.jpg', '631.jpg', '561.jpg', '604.jpg',
#          '568.jpg', '466.jpg', '697.jpg', '635.jpg', '706.jpg', '290.jpg', '633.jpg', '126.jpg', '239.jpg', '598.jpg',
#          '156.jpg', '234.jpg', '511.jpg', '258.jpg', '255.jpg', '407.jpg', '753.jpg', '299.jpg', '154.jpg', '737.jpg',
#          '257.jpg', '96.jpg', '597.jpg', '757.jpg', '766.jpg', '454.jpg', '389.jpg', '580.jpg', '339.jpg', '145.jpg',
#          '723.jpg', '367.jpg', '391.jpg', '162.jpg', '374.jpg', '118.jpg', '647.jpg', '53.jpg', '531.jpg', '589.jpg',
#          '178.jpg', '642.jpg', '383.jpg', '195.jpg', '213.jpg', '90.jpg', '26.jpg', '313.jpg', '73.jpg', '20.jpg',
#          '418.jpg', '148.jpg', '544.jpg', '463.jpg', '220.jpg', '27.jpg', '354.jpg', '167.jpg', '42.jpg', '516.jpg',
#          '398.jpg', '476.jpg', '426.jpg', '110.jpg', '527.jpg', '413.jpg', '329.jpg', '16.jpg', '159.jpg', '565.jpg',
#          '721.jpg', '2.jpg', '189.jpg', '430.jpg', '639.jpg', '214.jpg', '382.jpg', '498.jpg', '390.jpg', '128.jpg',
#          '545.jpg', '379.jpg', '285.jpg', '63.jpg', '709.jpg', '581.jpg', '556.jpg', '689.jpg', '618.jpg', '287.jpg',
#          '79.jpg', '370.jpg', '102.jpg', '494.jpg', '130.jpg', '410.jpg', '616.jpg', '349.jpg', '667.jpg', '450.jpg',
#          '232.jpg', '40.jpg', '763.jpg', '310.jpg', '701.jpg', '569.jpg', '739.jpg', '30.jpg', '357.jpg', '651.jpg',
#          '752.jpg', '303.jpg', '181.jpg', '415.jpg', '304.jpg', '560.jpg', '473.jpg', '225.jpg', '312.jpg', '711.jpg',
#          '607.jpg', '400.jpg', '49.jpg', '297.jpg', '113.jpg', '637.jpg', '638.jpg', '595.jpg', '7.jpg', '459.jpg',
#          '139.jpg', '478.jpg', '190.jpg', '457.jpg', '501.jpg', '218.jpg', '630.jpg', '8.jpg', '725.jpg', '3.jpg',
#          '45.jpg', '77.jpg', '662.jpg', '393.jpg', '34.jpg', '758.jpg', '458.jpg', '404.jpg', '550.jpg', '519.jpg',
#          '351.jpg', '748.jpg', '277.jpg', '449.jpg', '161.jpg', '221.jpg', '464.jpg', '396.jpg', '557.jpg', '366.jpg',
#          '43.jpg', '528.jpg', '343.jpg', '123.jpg', '21.jpg', '710.jpg', '622.jpg', '543.jpg', '215.jpg', '615.jpg',
#          '179.jpg', '677.jpg', '583.jpg', '579.jpg', '307.jpg', '24.jpg', '643.jpg', '293.jpg', '655.jpg', '755.jpg',
#          '603.jpg', '187.jpg', '327.jpg', '200.jpg', '109.jpg', '678.jpg', '352.jpg', '308.jpg', '266.jpg', '467.jpg',
#          '472.jpg', '423.jpg', '274.jpg', '504.jpg', '149.jpg', '636.jpg', '199.jpg', '540.jpg', '171.jpg', '207.jpg',
#          '587.jpg', '571.jpg', '174.jpg', '54.jpg', '240.jpg', '674.jpg', '634.jpg', '621.jpg', '733.jpg', '137.jpg',
#          '715.jpg', '507.jpg', '613.jpg', '452.jpg', '465.jpg', '691.jpg']
# name = ['Men Hybrid NX', 'Men  Walking Shoes', 'Men Flex Ccontrol || Training', 'Men Retro BasketBall Sneakers',
#         'Running Shoe', 'Men Out Black', 'Jordan Price', 'Imani Schwartz', 'Maggy Holder', 'Nomlanga Slater',
#         'Chaim Townsend', 'Amery Blackwell', 'Mallory Dudley', 'Stephen Ratliff', 'Cailin Ferrell', 'Autumn Fletcher',
#         'Stacey Lynn', 'Vance Schmidt', 'Shelly Macdonald', 'Richard Frye']
# caption = "Best Shoes From Karma Shoes Store"
# pid = [1, 2, 3, 4, 9, 14, 17, 20, 7, 8, 13, 11, 18, 5, 6, 10, 12, 15, 16, 19]
# count =0
#
# print(datetime.datetime.now())
# #
# conn = sqlite3.connect('db.sqlite3')
# print("Opened database successfully")
#     # print(random_date)
# for i in range(0,len(pid)):
#     for j in range(3):
#         nimg1 = choice(image)
#         img = Image.open('/home/ravi/Pictures/Picture Apparel/black_shoes/'+nimg1)
#         newimg = str(randint(10000, 99999)) + nimg1
#         s = "insert into Shopping_productphoto (photo, name, caption, pid_id,create_at,updated_at) values ('{}','{}','{}','{}','{}','{}')".format(newimg,name[i],caption,pid[i],datetime.datetime.now(),datetime.datetime.now())
#         print(s)
#         result = conn.execute(s)
#         print(result)
#         # print(result)
#         img.save('/home/ravi/Downloads/ShoppingMVC/static/media/' + newimg)
#         time.sleep(1)
# conn.close()
# print('done')
#
#
# # result = conn.execute("select id from Shopping_product")
# # conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
# #       VALUES (1, 'Paul', 32, 'California', 20000.00 )");
# # lt = []
# # for r in result:
# #     lt.append(r[0])
# # print(lt)
# #
# # print("Records created successfully")
# # conn.close()
#
# # lt = []
# # for root, dirs, files in os.walk("/home/ravi/Pictures/Picture Apparel/black_shoes/"):
# #     for filename in files:
# #         if '.jpg' in filename or '.png' in filename or '.webp' in filename:
# #             lt.append(filename)
# #             # img = Image.open(root+"/"+filename)
# #             # newimg = str(randint(10000,99999))+filename
# #             # print(newimg)
# #             # img.save('/home/ravi/Music/'+newimg)
# #         else:
# #             break
# # print(lt)

# lt = [1,2,4,5,3,7,8,9,7,77,43,2,324,34,67,6,65,3]
# print(lt[:8:-1])
