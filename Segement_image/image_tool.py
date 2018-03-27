from  PIL import Image
import os



class Image_tool(object):

    #to get a binarized table
    def get_bin_table(self,threshold = 140):

        table =[]
        for i in range(256):
            if i > threshold:
                table.append(1)
            else:
                table.append(0)


        return table


    #to sum the neigibor

    def sum_9_region(self,img,x,y):
        cur_pixel = img.getpixel((x,y))

        width = img.width
        height = img.height
        if cur_pixel == 1:
            return 0

        #process the pixel's neighbor
        if y == 0:  # 第一行
            if x == 0:  # 左上顶点,4邻域
                # 中心点旁边3个点
                sum = cur_pixel \
                      + img.getpixel((x, y + 1)) \
                      + img.getpixel((x + 1, y)) \
                      + img.getpixel((x + 1, y + 1))
                return 4 - sum
            elif x == width - 1:  # 右上顶点
                sum = cur_pixel \
                      + img.getpixel((x, y + 1)) \
                      + img.getpixel((x - 1, y)) \
                      + img.getpixel((x - 1, y + 1))

                return 4 - sum
            else:  # 最上非顶点,6邻域
                sum = img.getpixel((x - 1, y)) \
                      + img.getpixel((x - 1, y + 1)) \
                      + cur_pixel \
                      + img.getpixel((x, y + 1)) \
                      + img.getpixel((x + 1, y)) \
                      + img.getpixel((x + 1, y + 1))
                return 6 - sum
        elif y == height - 1:  # 最下面一行
            if x == 0:  # 左下顶点
                # 中心点旁边3个点
                sum = cur_pixel \
                      + img.getpixel((x + 1, y)) \
                      + img.getpixel((x + 1, y - 1)) \
                      + img.getpixel((x, y - 1))
                return 4 - sum
            elif x == width - 1:  # 右下顶点
                sum = cur_pixel \
                      + img.getpixel((x, y - 1)) \
                      + img.getpixel((x - 1, y)) \
                      + img.getpixel((x - 1, y - 1))

                return 4 - sum
            else:  # 最下非顶点,6邻域
                sum = cur_pixel \
                      + img.getpixel((x - 1, y)) \
                      + img.getpixel((x + 1, y)) \
                      + img.getpixel((x, y - 1)) \
                      + img.getpixel((x - 1, y - 1)) \
                      + img.getpixel((x + 1, y - 1))
                return 6 - sum
        else:  # y不在边界
            if x == 0:  # 左边非顶点
                sum = img.getpixel((x, y - 1)) \
                      + cur_pixel \
                      + img.getpixel((x, y + 1)) \
                      + img.getpixel((x + 1, y - 1)) \
                      + img.getpixel((x + 1, y)) \
                      + img.getpixel((x + 1, y + 1))

                return 6 - sum
            elif x == width - 1:  # 右边非顶点
                # print('%s,%s' % (x, y))
                sum = img.getpixel((x, y - 1)) \
                      + cur_pixel \
                      + img.getpixel((x, y + 1)) \
                      + img.getpixel((x - 1, y - 1)) \
                      + img.getpixel((x - 1, y)) \
                      + img.getpixel((x - 1, y + 1))

                return 6 - sum
            else:  # 具备9领域条件的
                sum = img.getpixel((x - 1, y - 1)) \
                      + img.getpixel((x - 1, y)) \
                      + img.getpixel((x - 1, y + 1)) \
                      + img.getpixel((x, y - 1)) \
                      + cur_pixel \
                      + img.getpixel((x, y + 1)) \
                      + img.getpixel((x + 1, y - 1)) \
                      + img.getpixel((x + 1, y)) \
                      + img.getpixel((x + 1, y + 1))
                return 9 - sum

        return 9 -sum

    def remove_noise_pixel(self,img,noise_point_list):

        for item in noise_point_list:
            img.putpixel((item[0],item[1]),1)


    #get a image with noise
    def get_clear_bin_image(self,img):

        imgry = img.convert('L')

        table = self.get_bin_table()
        out = imgry.point(table,'1') #get a binarized image


        noise_point_list = []

        for x in range(out.width):
            for y in range(out.height):
                res_9 = self.sum_9_region(out,x,y)


                if (0 < res_9 < 3 ) and out.getpixel((x,y)) ==0:
                    pos = (x,y)
                    noise_point_list.append(pos)

        self.remove_noise_pixel(out,noise_point_list)

        return out

    #segement the picture
    def get_crop_img(self,img):

        child_img_list = []

        for i in range(4):

            x = 2 + i * (6 + 4)
            y = 0
            child_img = img.crop((x,y,x + 6,y + 10))
            child_img_list.append(child_img)

        return child_img_list


test = Image_tool()
img = Image.open("./test1.png")
imgry = test.get_clear_bin_image(img)
imgry.save("test3.jpg")
child_img_list = test.get_crop_img(imgry)
child_img_list[2].save("test1-2.jpg")
