package edu.gatech.cse6242;

import java.io.IOException;
import java.util.StringTokenizer;
import java.lang.Object;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class Q1 {
	
  public static class TempMapper 
      extends Mapper<Object, Text, IntWritable, IntWritable>{

    private IntWritable target = new IntWritable();
    private IntWritable weight = new IntWritable();

  	public void map(Object key, Text value, Context context)
  			throws IOException, InterruptedException{
  					//split each line of data
  					StringTokenizer itr = new StringTokenizer(value.toString(),"\n");
            while (itr.hasMoreTokens()){
              String line = itr.nextToken();
              String[] tokens = line.split("\t");

              //extract the target and weight
              target.set(Integer.parseInt(tokens[1]));
              weight.set(Integer.parseInt(tokens[2]));

              //write into Mapper output
              context.write(target, weight); 
            }
  				}
  			}
  
  public static class TempReducer
      extends Reducer<IntWritable,IntWritable,IntWritable,IntWritable>{

  	private IntWritable result = new IntWritable();

  	public void reduce(IntWritable key, Iterable<IntWritable> values, Context context) 
  			throws IOException, InterruptedException{
  					//intital the sum
  					int sum = 0;

  					//compute the sum
  					for (IntWritable val: values) {
  						sum += val.get();
  					}
  					result.set(sum);
  					//write into Reducer output
  					context.write(key, result);
  				}
  		}

  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "Q1");

    /* TODO: Needs to be implemented */
	//set this class to Jar
    job.setJarByClass(Q1.class);

	  //assgin the two class designed as the class to process job
    job.setMapperClass(TempMapper.class);
    job.setCombinerClass(TempReducer.class);
    job.setReducerClass(TempReducer.class);

    //set up the class of key and value in output file
    job.setOutputKeyClass(IntWritable.class);
    job.setOutputValueClass(IntWritable.class);

    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }

}
