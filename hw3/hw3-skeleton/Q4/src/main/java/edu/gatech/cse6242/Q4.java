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
import java.io.IOException;

public class Q4 {

	public static class DegreediffMapper extends Mapper<Object, Text, Text, IntWritable>{
		
		private Text node = new Text();
		private IntWritable out_degree = new IntWritable(1);
		private IntWritable in_degree = new IntWritable(-1);

		public void map(Object key, Text value, Context context) throws IOException, InterruptedException{
			
			String [] lines = value.toString().split("\t");
			
			if(lines.length == 2){
				node.set(lines[0]);
				context.write(node, out_degree);
				node.set(lines[1]);
				context.write(node, in_degree);
			}
		}
	}

	public static class FreqMapper extends Mapper<Object, Text, Text, IntWritable>{

		private IntWritable counter = new IntWritable(1);
		private Text freq = new Text();

		public void map(Object key, Text value, Context context) throws IOException, InterruptedException{

			String [] lines = value.toString().split("\t");

			if(lines.length == 2){
				freq.set(lines[1]);
				context.write(freq, counter);
			}
		}
	}

	public static class SumReducer extends Reducer<Text, IntWritable, Text, IntWritable>{

		private IntWritable result = new IntWritable();

		public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException{
            //intital the sum
			int sum = 0;

            //compute the sum
			for(IntWritable value : values){
				sum += value.get();
			}
			result.set(sum);
            //write into Reducer output
			context.write(key, result);
		}
	}

	public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();
		Job job1 = Job.getInstance(conf, "Q4_1");

		/* TODO: Needs to be implemented */
		//job1- first mapreduce job
		job1.setJarByClass(Q4.class);
		job1.setMapperClass(DegreediffMapper.class);
		job1.setCombinerClass(SumReducer.class);
		job1.setReducerClass(SumReducer.class);
		job1.setOutputKeyClass(Text.class);
		job1.setOutputValueClass(IntWritable.class);
		
		FileInputFormat.addInputPath(job1, new Path(args[0]));
		FileOutputFormat.setOutputPath(job1, new Path("output_1"));

		job1.waitForCompletion(true);

		//job2- second mapreduce job
		Job job2 = Job.getInstance(conf, "Q4_2");

		job2.setJarByClass(Q4.class);
		job2.setMapperClass(FreqMapper.class);
		job2.setCombinerClass(SumReducer.class);
		job2.setReducerClass(SumReducer.class);
		job2.setOutputKeyClass(Text.class);
		job2.setOutputValueClass(IntWritable.class);


		FileInputFormat.addInputPath(job2, new Path("output_1"));
		FileOutputFormat.setOutputPath(job2, new Path(args[1]));
		System.exit(job2.waitForCompletion(true) ? 0 : 1);
	}
}
