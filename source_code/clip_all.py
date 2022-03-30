# -*- coding: utf-8 -*-
# 裁剪遥感影
# parameters: size

from osgeo import gdal
import os

# def get_image_numer(dir_path):
#     image_files = os.listdir(dir_path)
#     # image_files.sort(key = lambda x:int(x[:-4]))

#     #初始化，如果一开始裁剪影像路径里是空的
#     if len(image_files) == 0:
#         true_number = 0
#     #用来获取最后一张图片的标号
#     else:
#         image_number = len(image_files)
#         image_last_name = image_files[image_number-1]
#         index = image_last_name.find('.') 
#         true_number = int(image_last_name[:index])
#     return true_number

def clip_image(original_file_name,clip_image_dir):
    num = 1
    # num = get_image_numer(clip_image_dir) + 1     #计数器，计算文件名的编号
    in_ds = gdal.Open(original_file_name)              # 读取要切的原图
    width = in_ds.RasterXSize                         # 获取数据宽度   
    height = in_ds.RasterYSize                        # 获取数据高度
    outbandsize = in_ds.RasterCount                   # 获取数据波段数
    im_geotrans = in_ds.GetGeoTransform()             # 获取仿射矩阵信息
    im_proj = in_ds.GetProjection()                   # 获取投影信息
    datatype = in_ds.GetRasterBand(1).DataType  
    im_data = in_ds.ReadAsArray()                     #获取数据 

    prefix = original_file_name.split('/')[2].split('.')[0]
    # 读取原图中的每个波段
    in_band1 = in_ds.GetRasterBand(1)
    # in_band2 = in_ds.GetRasterBand(2)
    # in_band3 = in_ds.GetRasterBand(3)

    # 定义切图的起始点坐标
    offset_x = 0  
    offset_y = 0

    # 定义切图的大小（矩形框）
    size = 8000             # 这里设置裁剪的尺寸，这个程序因为我原来有好多图，所以要批量裁剪。
    col_num = int(width / size)  #宽度可以分成几块
    row_num = int(height / size) #高度可以分成几块
    if(width % size != 0):
        col_num += 1
    if(height % size != 0):
        row_num += 1    

    
    for i in range(row_num):    #从高度下手！！！ 可以分成几块！
        for j in range(col_num):
            offset_x = i * size 
            offset_y = j * size
            ## 从每个波段中切需要的矩形框内的数据(注意读取的矩形框不能超过原图大小)
            b_ysize = min(width - offset_y, size)
            b_xsize = min(height - offset_x, size)


            out_band1 = in_band1.ReadAsArray(offset_y, offset_x, b_ysize, b_xsize)
            # out_band2 = in_band2.ReadAsArray(offset_y, offset_x, b_ysize, b_xsize)
            # out_band3 = in_band3.ReadAsArray(offset_y, offset_x, b_ysize, b_xsize)
            # 获取Tif的驱动，为创建切出来的图文件做准备
            gtif_driver = gdal.GetDriverByName("GTiff")
            file = clip_image_dir + prefix + '_' + str(num) + '.tif'
            num += 1 
            # 创建切出来的要存的文件
            out_ds = gtif_driver.Create(file, b_ysize, b_xsize, outbandsize, datatype)

            # 获取原图的原点坐标信息
            ori_transform = in_ds.GetGeoTransform()

            # 读取原图仿射变换参数值
            top_left_x = ori_transform[0]  # 左上角x坐标
            w_e_pixel_resolution = ori_transform[1] # 东西方向像素分辨率
            top_left_y = ori_transform[3] # 左上角y坐标
            n_s_pixel_resolution = ori_transform[5] # 南北方向像素分辨率

            # 根据反射变换参数计算新图的原点坐标
            top_left_x = top_left_x + offset_y * w_e_pixel_resolution
            top_left_y = top_left_y + offset_x * n_s_pixel_resolution

            # 将计算后的值组装为一个元组，以方便设置
            dst_transform = (top_left_x, ori_transform[1], ori_transform[2], top_left_y, ori_transform[4], ori_transform[5])

            # 设置裁剪出来图的原点坐标
            out_ds.SetGeoTransform(dst_transform)

            # 设置SRS属性（投影信息）
            out_ds.SetProjection(in_ds.GetProjection())

            # 写入目标文件
            out_ds.GetRasterBand(1).WriteArray(out_band1)
            # out_ds.GetRasterBand(2).WriteArray(out_band2)
            # out_ds.GetRasterBand(3).WriteArray(out_band3)
            # 将缓存写入磁盘
            out_ds.FlushCache()
            # del out_ds,out_band1,out_band2,out_band3
    num += 1
if __name__ == "__main__":
    
    #原始影像的路径
    original_image_dir = './all_image/'    
    original_image_files = os.listdir(original_image_dir)

    #裁剪影像的路径
    clip_image_dir = './14clip/'
    if os.path.exists(clip_image_dir):
        pass
    else:
        os.mkdir(clip_image_dir)

    for i in range(len(original_image_files)):
        original_file_name = os.path.join(original_image_dir,original_image_files[i])
        clip_image(original_file_name,clip_image_dir)