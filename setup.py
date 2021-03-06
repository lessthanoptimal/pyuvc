import os, platform
import numpy

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import glob

libs = []
extra_link_args = []
if platform.system() == 'Darwin':
    try:
        tj_lib = '/usr/local/opt/jpeg-turbo/lib/libturbojpeg.a'
    except IndexError:
       raise Exception("Please install libturbojpeg")
elif platform.system() == 'Linux':
    try:
        #check for tubo jpeg offical lib and select appropriate lib32/lib64 path.
        tj_lib = glob.glob('/opt/libjpeg-turbo/lib*')[0]+'/libturbojpeg.a'
    except IndexError:
       raise Exception("Please install libturbojpeg")
    libs  = ['rt']
    extra_link_args = ['-Wl,-R/usr/local/lib/']
elif platform.system() == 'Windows':
    raise NotImplementedError("please fix me.")


extensions = [
    Extension(  name="uvc",
                sources=['uvc.pyx'],
                include_dirs =  [numpy.get_include(),'/usr/local/opt/jpeg-turbo/include/'],
                libraries = ['uvc',]+libs,
                extra_link_args=extra_link_args,
                extra_objects = [tj_lib],
                extra_compile_args=[]
            ),
]

setup(  name="uvc",
        version="0.1", #make sure this is the same in v4l2.pxy
        description="Usb Video Class Device bindings with format conversion tool.",
        ext_modules=cythonize(extensions)
)
