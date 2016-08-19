<HTML>
   <BODY>
      
       <?
         $Uname = $_POST["unametxt"];
         $fh = fopen('front_end.txt','r');
         $flag = 0;  
         while ($line = fgets($fh)) 
           {
          
             if(strcmp($line,"%%\n")==0)
            {
              $line = fgets($fh);
              if(strcmp($line,$Uname."\n")==0) 
             {  
              print("Hi $Uname! <BR>");
              $flag =1;
              break;
             }
             else
             $flag = 0;
            } 
             
           }
         if($flag == 0)
         print("Doesnt exist"); 
         fclose($fh);
         
       ?>
       <br/>
       List of Tweets<br/>
       <ol id="listtweets" name = "listtweets">
       <?
         $Uname = $_POST["unametxt"];
         $fh = fopen('front_end.txt','r');
         $flag = 0;
         $count = 0;  
         while ($line = fgets($fh)) 
           {
          
             if(strcmp($line,"%%\n")==0)
            {
              $line = fgets($fh);
              $count++;
              if(strcmp($line,$Uname."\n")==0) 
              {  
               $line = fgets($fh);
               print("<li>$line</li>");
               while(strcmp($line,"%%\n")!=0 and $count<=20)
               {
                   print("<li>$line</li>");
                   $line = fgets($fh);
                   $count++;

               }
               $flag=1;
               break;
              }
              else
              $flag = 0;
            } 
             
           }
         if($flag == 0)
         print("Doesnt exist"); 
         fclose($fh);

       ?>
       </ol>
       List of Similar Users<br/>
       <ol id="listsimilar" name ="listsimilar">
       <?
         $Uname = $_POST["unametxt"];
         if (isset($_POST['btnkmeans'])) 
          {
            $fh = fopen('KMeansOp.txt','r');
            $line = fgets($fh);
            $flag = 0;
            $count = 0;  
              while ($line = fgets($fh)) 
               {
                $words = explode("\t", $line);
             
                if(strcmp($words[0],"\"$Uname\"")==0)
                {
                $flag = 1;
                $searchindex = $words[1];
                break;
                }
                else
                $flag = 0; 
             
              }
             if($flag == 0)
             print("Doesnt exist"); 
            fclose($fh);
            $fh = fopen('KMeansOp.txt','r');  
            $line = fgets($fh);
            if($flag == 1)
            {
                while ($line = fgets($fh))
                {
                   $words = explode("\t", $line);
                   if((strcmp($words[1],$searchindex) == 0) and strcmp($words[0],"\"$Uname\"") != 0)
                    {
                         print($words[0]);
                         print("<br>");
                    }                  
                }  
                 
            }
       
            fclose($fh);
           }
         else 
         {
            $fh = fopen('PFOp.txt','r');
            $line = fgets($fh);
            $flag = 0;
            $count = 0;  
              while ($line = fgets($fh)) 
               {
                $words = explode("\t", $line);
             
                if(strcmp($words[0],"\"$Uname\"")==0)
                {
                $flag = 1;
                $searchindex = $words[1];
                break;
                }
                else
                $flag = 0; 
             
              }
             if($flag == 0)
             print("Doesnt exist"); 
            fclose($fh);
            $fh = fopen('PFOp.txt','r');  
            $line = fgets($fh);
            if($flag == 1)
            {
                while ($line = fgets($fh))
                {
                   $words = explode("\t", $line);
                   if((strcmp($words[1],$searchindex) == 0) and strcmp($words[0],"\"$Uname\"") != 0)
                    {
                         print($words[0]);
                         print("<br>");
                    }                  
                }  
                 
            }
       
            fclose($fh);
          }
         

       ?>
       </ol>


    </BODY>
</HTML>




