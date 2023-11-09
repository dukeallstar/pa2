import unittest
from vec3 import vec3
import numpy as np
from color import color
from vec3 import vec3 as point3
from ray import ray
from interval import interval
from hittable import sphere
from hittable_list import hittable_list
from hit_record import hit_record
from camera import camera
from materials import lambertian,metal,dielectric

class TestMaterials(unittest.TestCase):

    def testlambertian(self):
		a = lambertian(color(1,0,1))
		origin = point3(1,1,1)
		direction = vec3(1,7,8)
		in_ray = ray(origin,direction)
		scattered = ray(origin,direction)
		record  = hit_record()
        record.p = point3(0,0,0)
        record.normal = vec3(0,0,1)
		color atten  = color(0.2,0.2,0.2) 
		a.scatter(ray_in,record,atten,scattered)
		self.assertEqual(record.p.x(),scattered.origin().x())
		self.assertEqual(record.p.y(),scattered.origin().y())
		self.assertEqual(record.p.z(),scattered.origin().z())
		
		self.assertEqual(-0.63523962690880742,scattered.direction().x())
		self.assertEqual(-0.74675177887748911,scattered.direction().y())
		self.assertEqual(0.80294062532306487,scattered.direction().z())

    def testmetal(self):
		a = metal(color(1,0,1),.3)
		origin = point3(1,1,1)
		direction = vec3(1,7,8)
		ray_in = ray(origin,direction)
		scattered = ray(origin,direction)
		record  = hit_record() 
        record.p = point3(0,0,0)
        record.normal = vec3(0,0,1)
		atten  = color(0.2,0.2,0.2) 
		a.scatter(ray_in,record,atten,scattered)
		self.assertEqual(record.p.x(),scattered.origin().x())
		self.assertEqual(record.p.y(),scattered.origin().y())
		self.assertEqual(record.p.z(),scattered.origin().z())
		
		self.assertEqual(-0.05626434835975537,scattered.direction().x())
		self.assertEqual(0.4793691511844973,scattered.direction().y())
		self.assertEqual(-0.79577664009127647,scattered.direction().z())


    def testdielectric(self):
		dielectric a = dielectric(1.3)
		origin = point3(1,1,1)
		direction = vec3(1,7,8)
		ray_in = ray(origin,direction)
		scattered = ray(origin,direction)
		hit_record record  = hit_record() 
        record.p = point3(0,0,0)
        record.normal = vec3(0,0,1)
		atten  = color(0.2,0.2,0.2) 
		a.scatter(ray_in,record,atten,scattered)
		self.assertEqual(record.p.x(),scattered.origin().x())
		self.assertEqual(record.p.y(),scattered.origin().y())
		self.assertEqual(record.p.z(),scattered.origin().z())
		
		self.assertEqual(0.093658581158169399,scattered.direction().x())
		self.assertEqual(0.65561006810718581,scattered.direction().y())
		self.assertEqual(-0.74926864926535519,scattered.direction().z())


class TestCamera(unittest.TestCase):
	

    def testInitialize(self):
        c = camera()
        c.initialize() 
        self.assertEqual(1.0,c.aspect_ratio)
        self.assertEqual(100,c.image_width)
        self.assertEqual(10,c.samples_per_pixel)
        self.assertEqual(10,c.max_depth)
        self.assertEqual(90,c.vfov)
        self.assertEqual(0,c.defocus_angle)
        self.assertEqual(10,c.focus_dist)
        self.assertEqual(point3(0,0,-1).x(),c.lookfrom.x())
        self.assertEqual(point3(0,0,-1).y(),c.lookfrom.y())
        self.assertEqual(point3(0,0,-1).z(),c.lookfrom.z())
        self.assertEqual(point3(0,0,0).x(),c.lookat.x())
        self.assertEqual(point3(0,0,0).y(),c.lookat.y())
        self.assertEqual(point3(0,0,0).z(),c.lookat.z())
        self.assertEqual(point3(0,1,0).x(),c.vup.x())
        self.assertEqual(point3(0,1,0).y(),c.vup.y())
        self.assertEqual(point3(0,1,0).z(),c.vup.z())


    def testGetRay(self):
	    #set random seed to 42
	    c = camera()
        c.initialize() 
        r = c.get_ray(130,130)  
        self.assertEqual(0.0,r.origin().x())
        self.assertEqual(0.0,r.origin().y())
        self.assertEqual(-1.0,r.origin().z())
        self.assertEqual(-16.006693989597256,r.direction().x())
        self.assertEqual(-16.065992841497057,r.direction().y())
        self.assertEqual(10.0,r.direction().z())


    def testGetSquareSample(self):
		#set random seed to 144
	    c = camera()
        c.initialize() 
        v = c.pixel_sample_square()
        self.assertEqual(0.083333106152713277,v.x())
        self.assertEqual(-0.091526530496776087,v.y())
        self.assertEqual(0.0,v.z())


    def testGetDiskSample(self):
	#set random seed to 144	
        c = camera()
        c.initialize() 
        v = c.pixel_sample_disk(2.0)
        self.assertEqual(-0.3583317294716834,v.x())
        self.assertEqual(0.037235998734831799,v.y())
        self.assertEqual(0.0,v.z())


    def testGetRayColor(self):
		#set random seed to 144
        c = camera()
        c.initialize() 
        v = c.pixel_sample_disk(2.0)
        self.assertEqual(-0.3583317294716834,v.x())
        self.assertEqual(0.037235998734831799,v.y())
        self.assertEqual(0.0,v.z())


    def testSphereHitTest(self):
        #set random seed to 144
	    c = camera()
        c.initialize() 
		direct = vec3(1,7,8)
		orig = point3(0,0,0)	
		r = ray(orig,direct)
        s = sphere(point3(10,70,80),5,make_shared<lambertian>(color(0.7,0.7,1.0)))
        rc = c.ray_color(r,1000,s)	
		self.assertEqual(0.61969189831627691,rc.x())
		self.assertEqual(0.65181513898976606,rc.y())
		self.assertEqual(1.0,rc.z())



    def testRenderImage(self):
        # set random seed to 144 
	    c = camera()
        c.initialize() 
		direct = vec3(1,7,8)
		orig = point3(0,0,0)	
		r = ray(orig,direct)
        s = sphere(point3(10,70,80),5,make_shared<lambertian>(color(0.7,0.7,1.0)))
        c.render(s,"image.ppm")
        refImg = open("result.ppm",'r')
        genImg = open("image.ppm",'r')
        reflines = refImg.readlines() 
        genlines = genImg.readlines() 
        for i in range(0,len(reflines)):
            self.assertEqual(reflines[i],genlines[i])



if __name__ == '__main__':
    unittest.main()

