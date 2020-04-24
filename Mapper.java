import java.util.HashMap;
import java.io.FileReader;
import java.io.BufferedReader;
import java.io.IOException;

class Mapper{
    public static void main(String[] args) throws IOException
    {
        String filepath = args[0];
        int indexCol = Integer.parseInt(args[1]);
        int index = 0;
        HashMap<String, Integer> outputMap = new HashMap<>();
        System.out.println(getNthString("aasdf,fsdf,fsdf,sadfasdf,asdfasdf,asdf", 0));
        BufferedReader bufferedReader = new BufferedReader(new FileReader(filepath));


        String line = bufferedReader.readLine(); 
        while (line!=null)
        {
            String c = getNthString(line, indexCol); 
            
            if (!outputMap.containsKey(c))
            {
                outputMap.put(c, index);
                index ++; System.out.println(index);
            }
        line = bufferedReader.readLine();
        }
        System.out.println(outputMap);
        bufferedReader.close();

    }
    private static String getNthString(String line, int indexCol)
    {
        StringBuilder stringBuilder = new StringBuilder();
        int countComma = 0;
        for (int i = 0; i < line.length(); i++)
        {
            String s = line.substring(i, i+1);
           if (s.equals(","))
           {
               countComma += 1;
               if (countComma > indexCol)
               {
                   return stringBuilder.toString();
               }
               continue;
           }
           if (countComma == indexCol)
           {
               stringBuilder.append(s);
           }
        }
        return stringBuilder.toString();
    }

}