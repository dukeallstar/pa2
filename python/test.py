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
from material import lambertian,metal,dielectric
from color import color
import random

class TestMaterials(unittest.TestCase):

    def testlambertian(self):
        random.seed(42) 
        a = lambertian(color(1,0,1))
        origin = point3(1,1,1)
        direction = vec3(1,7,8)
        ray_in = ray(origin,direction)
        scattered = ray(origin,direction)
        record  = hit_record()
        record.p = point3(0,0,0)
        record.normal = vec3(0,0,1)
        atten  = color(0.2,0.2,0.2) 
        res,scattered,atten =a.scatter(ray_in,record)
        self.assertEqual(record.p.x(),scattered.origin().x())
        self.assertEqual(record.p.y(),scattered.origin().y())
        self.assertEqual(record.p.z(),scattered.origin().z())

        self.assertAlmostEqual(-0.7818442803709916,scattered.direction.x(),2)
        self.assertAlmostEqual(-0.028800780236799862,scattered.direction.y(),2)
        self.assertAlmostEqual(0.377191814192429,scattered.direction.z(),2)

    def testmetal(self):
        
        random.seed(42)
        a = metal(color(1,0,1),.3)
        origin = point3(1,1,1)
        direction = vec3(1,7,8)
        ray_in = ray(origin,direction)
        scattered = ray(origin,direction)
        record  = hit_record() 
        record.p = point3(0,0,0)
        record.normal = vec3(0,0,1)
        atten  = color(0.2,0.2,0.2) 
        res,scattered,atten = a.scatter(ray_in,record)
        self.assertAlmostEqual(record.p.x(),scattered.origin().x())
        self.assertAlmostEqual(record.p.y(),scattered.origin().y())
        self.assertAlmostEqual(record.p.z(),scattered.origin().z())

        self.assertAlmostEqual( -0.16101711745797503,scattered.direction.x(),2)
        self.assertAlmostEqual(0.9351774918261945,scattered.direction.y(),2)
        self.assertAlmostEqual(-0.8911169485235475,scattered.direction.z(),2)


    def testdielectric(self):
        a = dielectric(1.3)
        origin = point3(1,1,1)
        direction = vec3(1,7,8)
        ray_in = ray(origin,direction)
        scattered = ray(origin,direction)
        record  = hit_record() 
        record.p = point3(0,0,0)
        record.normal = vec3(0,0,1)
        atten  = color(0.2,0.2,0.2) 
        res,scattered,atten=a.scatter(ray_in,record)
        self.assertAlmostEqual(record.p.x(),scattered.origin().x(),2)
        self.assertAlmostEqual(record.p.y(),scattered.origin().y(),2)
        self.assertAlmostEqual(record.p.z(),scattered.origin().z(),2)

        self.assertAlmostEqual(0.093658581158169399,scattered.direction.x(),2)
        self.assertAlmostEqual(0.65561006810718581,scattered.direction.y(),2)
        self.assertAlmostEqual(-0.74926864926535519,scattered.direction.z(),2)


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
        random.seed(42)
        c = camera()
        c.initialize() 
        r = c.get_ray(130,130)  
        self.assertEqual(0.0,r.origin().x())
        self.assertEqual(0.0,r.origin().y())
        self.assertEqual(-1.0,r.origin().z())
        self.assertAlmostEqual( -16.12788535969157,r.direction.x(),2)
        self.assertAlmostEqual(-16.00500215104453,r.direction.y(),2)
        self.assertEqual(10.0,r.direction.z())


    def testGetSquareSample(self):
		#set random seed to 144
        random.seed(42)
        c = camera()
        c.initialize() 
        v = c.pixel_sample_square()
        self.assertAlmostEqual(-0.027885359691576742,v.x(),2)
        self.assertAlmostEqual(0.09499784895546659,v.y(),2)
        self.assertEqual(0.0,v.z())


    def testGetDiskSample(self):
	#set random seed to 144	
        random.seed(42)
        c = camera()
        c.initialize() 
        v = c.pixel_sample_disk(2.0)
        self.assertAlmostEqual(0.2218702794464577,v.x(),2)
        self.assertAlmostEqual( 0.008173030512396505,v.y(),2)
        self.assertEqual(0.0,v.z())


    def testSphereHitTest(self):
        #set random seed to 144
        random.seed(42)
        c = camera()
        c.initialize() 
        direct = vec3(1,7,8)
        orig = point3(0,0,0)	
        r = ray(orig,direct)
        s = sphere(point3(10,70,80),5,lambertian(color(0.7,0.7,1.0)))
        rc = c.ray_color(r,1000,s)	
        self.assertAlmostEqual(0.5928344685594874,rc.x(),2)
        self.assertAlmostEqual(0.6357006811356924,rc.y(),2)
        self.assertEqual(1.0,rc.z())



    def testRenderImage(self):
        # set random seed to 144 
        random.seed(42)
        c = camera()
        c.initialize() 
        direct = vec3(1,7,8)
        orig = point3(0,0,0)	
        r = ray(orig,direct)
        s = sphere(point3(10,70,80),5,lambertian(color(0.7,0.7,1.0)))
        c.render(s,"image.ppm")
        refImg = open("py_result.ppm",'r')
        genImg = open("image.ppm",'r')
        reflines = refImg.readlines() 
        genlines = genImg.readlines() 
        for i in range(0,len(reflines)):
            self.assertEqual(reflines[i],genlines[i])

        refImg.close()
        genImg.close()


if __name__ == '__main__':
    unittest.main()

