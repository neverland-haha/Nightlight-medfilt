import os  
from osgeo import gdal
import numpy as np
import time
start = time.time()

if __name__ == '__main__':
    image_dir = './14clip/'
    #文件夹里的文件
    image_file = [file for file in os.listdir(image_dir) if '_9' in file] 
    save_info_image_name = os.path.join(image_dir,image_file[0])
    # 打开第一张 tif 图存储一下信息
    save_info_image = gdal.Open(save_info_image_name)    
    RasterXSize = save_info_image.RasterXSize
    RasterYSize = save_info_image.RasterYSize
    outband_size = 1
    geotrans = save_info_image.GetGeoTransform()                    # 这里第一个图像用来存放信息，其余的都用来 append 矩阵的值
    projection = save_info_image.GetProjection()
    DataType = save_info_image.GetRasterBand(1).DataType
    result_array = []

    for i in range(len(image_file)):
        # 开始的第一个图像存储一下信息
        if i == 0:
            save_info_image_array = save_info_image.ReadAsArray()
            result_array.append(save_info_image_array)
            del save_info_image_array                               # 处理的时候实时释放内存，否则爆内存太正常
        # 否则的话就一直打开 append
        else:
            image_name = os.path.join(image_dir,image_file[i])
            new_image = gdal.Open(image_name)
            new_image_array = new_image.ReadAsArray()       
            result_array.append(new_image_array)
            del new_image_array                                     # 处理的时候实时释放内存，否则爆内存太正常
            
    result = np.array(result_array)
    final_result = np.stack(result,axis=0)
    del result
    real_result = np.median(final_result,axis=0)
    del final_result
    # 创建一个矩阵
    gtif_driver = gdal.GetDriverByName("GTiff")
    out_file_name = './median_filt/2014_medfilt_9.tif'                  
    out_ds = gtif_driver.Create(out_file_name,RasterXSize,RasterYSize,outband_size,DataType)
    out_ds.SetProjection(projection)
    out_ds.SetGeoTransform(geotrans)
    out_ds.GetRasterBand(1).WriteArray(real_result)
    out_ds.FlushCache()
    del out_ds
    stop = time.time()
    print('完成一幅图像滤波的时间为: ' + str(stop-start) + "秒")