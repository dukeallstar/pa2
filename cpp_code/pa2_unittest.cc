#include <gtest/gtest.h>
#include "utils.h"
#include "vec3.h"
#include "color.h"
#include "interval.h"
#include "hittable.h"
#include "hittable_list.h"
#include "sphere.h"
#include "material.h"
#define private public
#include "camera.h"
#include <string>       // std::string
#include <iostream>     // std::cout
#include <sstream>      // std::stringstream
#include <fstream>
namespace {
	TEST(Oneb,Lambertian){
		srand(42);
		lambertian a = lambertian(color(1,0,1));
		point3 origin = point3(1,1,1);
		vec3 direction = vec3(1,7,8);
		ray in = ray(origin,direction);
		ray scattered = ray(origin,direction);
		hit_record record  = hit_record();
    record.p = point3(0,0,0);
    record.normal = vec3(0,0,1);
		color atten  = color(0.2,0.2,0.2); 
		a.scatter(in,record,atten,scattered);
		EXPECT_EQ(record.p.x(),scattered.origin().x());
		EXPECT_EQ(record.p.y(),scattered.origin().y());
		EXPECT_EQ(record.p.z(),scattered.origin().z());
		
		EXPECT_EQ(-0.63523962690880742,scattered.direction().x());
		EXPECT_EQ(-0.74675177887748911,scattered.direction().y());
		EXPECT_EQ(0.80294062532306487,scattered.direction().z());
	}

	TEST(Onec,Metal){
		srand(42);
		metal a = metal(color(1,0,1),.3);
		point3 origin = point3(1,1,1);
		vec3 direction = vec3(1,7,8);
		ray in = ray(origin,direction);
		ray scattered = ray(origin,direction);
		hit_record record  = hit_record(); 
    record.p = point3(0,0,0);
    record.normal = vec3(0,0,1);
		color atten  = color(0.2,0.2,0.2); 
		a.scatter(in,record,atten,scattered);
		EXPECT_EQ(record.p.x(),scattered.origin().x());
		EXPECT_EQ(record.p.y(),scattered.origin().y());
		EXPECT_EQ(record.p.z(),scattered.origin().z());
		
		EXPECT_EQ(-0.05626434835975537,scattered.direction().x());
		EXPECT_EQ(0.4793691511844973,scattered.direction().y());
		EXPECT_EQ(-0.79577664009127647,scattered.direction().z());
	}


	TEST(Oned,Dielectric){
		srand(42);
		dielectric a = dielectric(1.3);
		point3 origin = point3(1,1,1);
		vec3 direction = vec3(1,7,8);
		ray in = ray(origin,direction);
		ray scattered = ray(origin,direction);
		hit_record record  = hit_record(); 
    record.p = point3(0,0,0);
    record.normal = vec3(0,0,1);
		color atten  = color(0.2,0.2,0.2); 
		a.scatter(in,record,atten,scattered);
		EXPECT_EQ(record.p.x(),scattered.origin().x());
		EXPECT_EQ(record.p.y(),scattered.origin().y());
		EXPECT_EQ(record.p.z(),scattered.origin().z());
		
		EXPECT_EQ(0.093658581158169399,scattered.direction().x());
		EXPECT_EQ(0.65561006810718581,scattered.direction().y());
		EXPECT_EQ(-0.74926864926535519,scattered.direction().z());
	}


	TEST(Twob,Init){
		srand(42);
	 camera c = camera();
    c.initialize(); 
    EXPECT_EQ(1.0,c.aspect_ratio);
    EXPECT_EQ(100,c.image_width);
    EXPECT_EQ(10,c.samples_per_pixel);
    EXPECT_EQ(10,c.max_depth);
    EXPECT_EQ(90,c.vfov);
    EXPECT_EQ(0,c.defocus_angle);
    EXPECT_EQ(10,c.focus_dist);
    EXPECT_EQ(point3(0,0,-1).x(),c.lookfrom.x());
    EXPECT_EQ(point3(0,0,-1).y(),c.lookfrom.y());
    EXPECT_EQ(point3(0,0,-1).z(),c.lookfrom.z());
    EXPECT_EQ(point3(0,0,0).x(),c.lookat.x());
    EXPECT_EQ(point3(0,0,0).y(),c.lookat.y());
    EXPECT_EQ(point3(0,0,0).z(),c.lookat.z());
    EXPECT_EQ(point3(0,1,0).x(),c.vup.x());
    EXPECT_EQ(point3(0,1,0).y(),c.vup.y());
    EXPECT_EQ(point3(0,1,0).z(),c.vup.z());
	}


	TEST(Twoc,GetRay){
		srand(42);
	 camera c = camera();
    c.initialize(); 
    ray r = c.get_ray(130,130);  
    EXPECT_EQ(0.0,r.origin().x());
    EXPECT_EQ(0.0,r.origin().y());
    EXPECT_EQ(-1.0,r.origin().z());
    EXPECT_EQ(-16.006693989597256,r.direction().x());
    EXPECT_EQ(-16.065992841497057,r.direction().y());
    EXPECT_EQ(10.0,r.direction().z());
	}


	TEST(Twod,GetSquareSample){
		srand(144);
	 camera c = camera();
    c.initialize(); 
    vec3 v = c.pixel_sample_square();
    EXPECT_EQ(0.083333106152713277,v.x());
    EXPECT_EQ(-0.091526530496776087,v.y());
    EXPECT_EQ(0.0,v.z());
	}

	TEST(Twoe,GetDiskSample){
		srand(144);
	 camera c = camera();
    c.initialize(); 
    vec3 v = c.pixel_sample_disk(2.0);
    EXPECT_EQ(-0.3583317294716834,v.x());
    EXPECT_EQ(0.037235998734831799,v.y());
    EXPECT_EQ(0.0,v.z());
	}


	TEST(Twof,GetRayColor){
		srand(144);
	 camera c = camera();
    c.initialize(); 
    vec3 v = c.pixel_sample_disk(2.0);
    EXPECT_DOUBLE_EQ(-0.3583317294716834,v.x());
    EXPECT_DOUBLE_EQ(0.037235998734831799,v.y());
    EXPECT_DOUBLE_EQ(0.0,v.z());
	}


	TEST(SphereHitTest,Hit){

		srand(144);
	 camera c = camera();
    c.initialize(); 
		vec3 direct = vec3(1,7,8);
		point3 orig = point3(0,0,0);	
		ray r = ray(orig,direct);
    sphere s = sphere(point3(10,70,80),5,make_shared<lambertian>(color(0.7,0.7,1.0)));
	 color rc = c.ray_color(r,1000,s);	
		EXPECT_DOUBLE_EQ(0.61969189831627691,rc.x());
		EXPECT_DOUBLE_EQ(0.65181513898976606,rc.y());
		EXPECT_DOUBLE_EQ(1.0,rc.z());

	}

  
	TEST(RenderTest,ImageRender){
std::stringstream buffer;

// Save cout's buffer here
std::streambuf *sbuf = std::cout.rdbuf();

// Redirect cout to our stringstream buffer or any other ostream
std::cout.rdbuf(buffer.rdbuf());
		srand(144);
	 camera c = camera();
    c.initialize(); 
		vec3 direct = vec3(1,7,8);
		point3 orig = point3(0,0,0);	
		ray r = ray(orig,direct);
    sphere s = sphere(point3(10,70,80),5,make_shared<lambertian>(color(0.7,0.7,1.0)));
	 c.render(s);
    std::cout.rdbuf(sbuf);
    std::string image_string = buffer.str();
  std::cout << image_string;
std::ifstream t;
  t.open("result.txt");
std::stringstream buffer2;
buffer2 << t.rdbuf();
  std::string ref_image = buffer2.str();
  EXPECT_EQ(ref_image.compare(image_string),0);
	}



}



int main(int argc, char **argv) {
  printf("Running main() from %s\n", __FILE__);
  testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
