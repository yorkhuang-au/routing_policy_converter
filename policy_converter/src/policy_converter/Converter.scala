
package policy_converter

import scala.io.Source

object Converter {
  def main(args: Array[String]) {
    val c = new Converter("/home/yhuang/routing_policy_converter/policy_converter/data/rtaultifw03-192.168.12.52.txt")
    
  }
}

class Converter(filename : String) {
  def getHostnames(filename : String) = {
    Source.fromFile(filename).getLines
      .filter { _.startsWith("name ") }
      .map { t => val v = t.split(" ")
        (v(2) -> v(1))
      }.toMap
  }
  
  
                                                 
  val hostnames = getHostnames(filename)
  
  val lines2 = Source.fromFile(filename).getLines()
  //println( lines2.length )
  val t = lines2.mkString.split("!")
  val hostnames = t.take(1)
  .filter { _.startsWith("interface") }
    //.take(3).foreach(println)
  println(t)
  println("end of work")
    
}