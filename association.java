import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class association {
  public static void main(String []args){
	    String csvFile = "/Users/mengnanzhao/Documents/Research/Breast Cancer/data/10000messages.txt";
	    String csvFile1 = "/Users/mengnanzhao/Documents/Research/Breast Cancer/data/SymptomCHV.txt";
	    BufferedReader br = null;
	    BufferedReader br1 = null;
		String line = "";
		try {
			//read
			br = new BufferedReader(new FileReader(csvFile));
			br1 = new BufferedReader(new FileReader(csvFile1));
            
            //firstly, get the symptom CHV dictionary ready
            int N_symptom = 39;
            int [][]SymptomMatrix = new int[N_symptom][N_symptom];
            String []Symptoms = new String[N_symptom];
            int []SymptomCounts = new int[N_symptom];
            //initiate symptoms
            for(int i=0;i<Symptoms.length;i++){
            	SymptomCounts[i] = 0;
            }
            for(int i=0;i<Symptoms.length;i++){
            	Symptoms[i] = "";
            }
  		  	for(int i=0;i<Symptoms.length;i++){
  		  		for(int j=0;j<Symptoms.length;j++){
  		  			SymptomMatrix[i][j] = 0;
  		  		}
  		  	}
            //This is to get the symptom CHV word list, store word-symptom in SymptomDic, store symptom-counts in SymptomCounts
            //write to new file
		    File csv;
            csv=new File("/Users/mengnanzhao/Documents/Research/Breast Cancer/data/10000messages.json"); //  
  		  	BufferedWriter bw = new BufferedWriter(new FileWriter(csv, true));
            int row = 0;
            line = br1.readLine();
            while (line != null) {	
            	Symptoms[row] = line;    	//store the symptom+term string in each Symptoms[i]
            	row++;
            	line = br1.readLine();
            }

            String[][] symptomName = new String[39][40];     //save the symptom terms into a matrix
            for(int i = 0; i < 39; i++)
            {
            	String temp[] = Symptoms[i].split(":");
            	String terms[] = temp[1].split(",");
            	int size = terms.length;
            	if(size < 40)
            	{
            		for(int j = 0; j < size; j++)
            			symptomName[i][j] = terms[j].trim();
            		for(int j = size; j < 40;j++)
            			symptomName[i][j] = "0";
            	}
            }  
            //read the file of messages line by line
            line = br.readLine();
            while(line != null)
            {
           	//for each message, try to see if it contains any pair of symptoms
            	for(int i = 0;i<39;i++){
            		int flag_i = 0;
            		for(int k = 0;k < 40;k++){
            			if(line.replaceAll("_", " ").contains(symptomName[i][k])){
            				if(!symptomName[i][k].equals("0")){	
            					flag_i = 1;//symptom i is contained in the message
            					break;
            				}
            			}  
            		}
            		if(flag_i == 1){
            			for(int j = 0;j < 39;j++){
            				int flag_j = 0;
            				for(int k = 0;k < 40;k++){
            					if(line.replaceAll("_", " ").contains(symptomName[j][k])){
            						if(!symptomName[j][k].equals("0")){
            							flag_j = 1;//symptom j is contained in the message;
            							break;
            						}
            					}  			  
            				}
            				if(flag_j == 1)
            				{	SymptomMatrix[i][j] = SymptomMatrix[i][j] + 1;	}
            			}		
           		 	}
       		  	}
            	line = br.readLine();
            }
            
            //calculate the counts of each symptom
            for(int i = 0;i < Symptoms.length;i++){
  		  		SymptomCounts[i] = SymptomMatrix[i][i];
  		  	}
            for(int i = 0;i < 39;i++){
         		   SymptomMatrix[i][i] = 0;
            }
			for(int i = 0;i < 39;i++){
				for(int j = 0; j < 39; j++)
					System.out.print(SymptomMatrix[i][j] + ",");
	      	   	System.out.println("");
			}
          
          //write the node to the json file
         
          bw.write("{\n\"nodes\":[\n");

          
          //assign IDs to non-zero symptoms
          int []SymptomID=new int[N_symptom];
          //initiate
          for(int i = 0;i < Symptoms.length;i++){
        	  SymptomID[i]=-1;
          }
          row = 0;
          //assign IDs
          for(int i=0;i<Symptoms.length;i++){
		  		if(SymptomCounts[i]!=0){
		  			SymptomID[i]=row;
		  			row++;
		  		}	
		  }
        
          //write the node part of the json file, groups will be filled in later manually from the clustering results using RStudio
          int position = 0;
          //write the first node
          for(int i = 0;i < Symptoms.length;i++){
        	  if(SymptomCounts[i] != 0){
            	  String[] temp = Symptoms[i].split(":");
        		  bw.write("{\"name\":\""+temp[0]+"\",\"value\":"+SymptomCounts[i]+",\"group\":"+",\"centroid\":0}");
        		  position=i;
        		  break;
        	  }
          }
          //write the rest nodes
          for(int i = position + 1;i < Symptoms.length;i++){
        	  if(SymptomCounts[i] != 0){
            	  String[] temp = Symptoms[i].split(":");
        		  bw.write(",\n{\"name\":\""+temp[0]+"\",\"value\":"+SymptomCounts[i]+",\"group\":"+",\"centroid\":0}");
        	  }
          }
          //write the links
          bw.write("\n],\n\"links\":[");
          //write the first link
          if(SymptomMatrix[1][0] != 0){
        	  double similarity = (double)SymptomMatrix[1][0]/((double)SymptomCounts[1]*(double)SymptomCounts[0]);
        	  bw.write("{\"source\":1,\"target\":0,\"value\":"+(similarity)+"}");
		  }else{
			  bw.write("{\"source\":1,\"target\":0,\"value\":0"+"}");

		  }
          //write the rest links
          for(int i = 2;i < Symptoms.length;i++){
		  		for(int j = 0;j < i;j++){
		  			if(SymptomMatrix[i][j] != 0){
		  				//System.out.println("look!im not zero!"+SymtpomMatrix[i][j]);
		  				double similarity=(double)SymptomMatrix[i][j]/((double)SymptomCounts[i]*(double)SymptomCounts[j]);
		  	        	bw.write(",\n{\"source\":"+SymptomID[i]+",\"target\":"+SymptomID[j]+",\"value\":"+(similarity)+"}");
		  			}
		  			
		  		}
		  }
          bw.write("\n]\n}");
          
          //generate the distance matrix for clustering in RStudio, paste the output to a csv file
          System.out.print("The co-ocurrence divided by symptom counts\n");
          for(int i=0;i<Symptoms.length;i++){
        	  String temp[]=Symptoms[i].split(":");
        	  System.out.print(temp[0]+",");
        	  for(int j=0;j<Symptoms.length;j++){
        		  if(SymptomMatrix[i][j]!=0){			  
        			  double similarity=(double)SymptomMatrix[i][j]/((double)SymptomCounts[i]*(double)SymptomCounts[j]);
        			  System.out.print((1-(similarity))*(1-(similarity))+",");
        		  }else{
        			  System.out.print("1,");
        		  }
        		  
        	  }
        	  System.out.println("");
          }
          bw.close();
             
			
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} catch(Exception e){
			e.printStackTrace();
		}
  }
}


