
import scala.io.Source

object converter {
  println("Welcome to the Scala worksheet")       //> Welcome to the Scala worksheet

	val lines = Source.fromFile("/home/yhuang/routing_policy_converter/policy_converter/data/rtaultifw03-192.168.12.52.txt").getLines()
                                                  //> lines  : Iterator[String] = non-empty iterator
	
	

}