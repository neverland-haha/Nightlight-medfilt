# Nightlight-medfilt

1. 先用 `clip_all.py` 里的代码裁剪一下，依据后缀名判断是否为同一块图像不同时间的影像（记得改参数，如果地区小的话直接别裁剪了，直接中值去噪把）。
2. 用 `median_filt.py` 里的代码做个中值滤波，因为就写了半小时的代码，所以有些东西懒得设计了。讲道理，直接做一个文件夹里的所有图像计算应该是可以的。
3. 然后用 `combine.py` 里的文件做一个合并（如果地区小的话也没有这个问题了吧）

有啥问题，公众号里说，github 就是个小仓库，不咋看。
