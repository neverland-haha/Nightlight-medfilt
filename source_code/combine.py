from osgeo import gdal
import os

def combine_image(image_dir,warp_out_file_name,compressed_tif_file):
    """
    合并文件夹中的 GTif 图像，并且压缩,顺带着把拼接完成的未压缩的图像给删除。
    """
    image_path = []
    image_files = [file for file in os.listdir(image_dir) if file.endswith('.tif')]
    image_path = list(map(lambda image_file:image_dir + image_file,image_files))
    
    g = gdal.Warp(warp_out_file_name, image_path, format="GTiff")
    # 多波段到后面就可以停了，同时把 compressed_tif_file 形参也给注释掉。
    img_xsize = g.RasterXSize
    img_ysize = g.RasterYSize
    img_projection = g.GetProjection()
    img_geotransform = g.GetGeoTransform()
    datatype = g.GetRasterBand(1).DataType
    raster_band_size = g.RasterCount
    img_array = g.GetRasterBand(1).ReadAsArray()            # 这个代码就是 gdal.warp 做一个拼接，然后由于是一个 对象，然后要压缩一下。
    out_file_name = compressed_tif_file
    g_driver = gdal.GetDriverByName('GTiff')
    out_ds = g_driver.Create(out_file_name,img_xsize,img_ysize,raster_band_size,datatype,options = ['compress=lzw'])
    out_ds.SetProjection(img_projection)                        
    out_ds.SetGeoTransform(img_geotransform)
    out_ds.GetRasterBand(1).WriteArray(img_array)
    out_ds.FlushCache()
    del out_ds 
    os.remove(warp_out_file_name)
    
    
if __name__ == '__main__':
    # 需要拼接的图像的文件夹
    image_dir = './median_filt/'
    # gdal.warp 后的文件，未压缩，是 gdal.Datasets 的形式，但是有各种各样的信息。   
    warp_out_file_name = './uncompressed.tif'
    # 如果是多波段，LZW 压缩之后，可能会比原来的图还大，不如不压缩。
    compressed_tif_file = './compressed_combine.tif'
    combine_image(image_dir,warp_out_file_name,compressed_tif_file)