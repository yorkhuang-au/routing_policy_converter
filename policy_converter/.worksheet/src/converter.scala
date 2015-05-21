
import scala.io.Source

object converter {;import org.scalaide.worksheet.runtime.library.WorksheetSupport._; def main(args: Array[String])=$execute{;$skip(87); 
  println("Welcome to the Scala worksheet");$skip(134); 

	val lines = Source.fromFile("/home/yhuang/routing_policy_converter/policy_converter/data/rtaultifw03-192.168.12.52.txt").getLines();System.out.println("""lines  : Iterator[String] = """ + $show(lines ));$skip(24); 
	val hostnames = lines.;System.out.println("""hostnames  : <error> = """ + $show(hostnames ))}
	

}
