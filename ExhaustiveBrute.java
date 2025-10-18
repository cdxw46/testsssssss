import java.io.*;
import java.util.*;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class ExhaustiveBrute {
    public static final String FLAG = "S+kUZtaHEYpFpv2ixuTnqBdORNzsdVJrAxWznyOljEo=";
    
    public static void main(String[] args) throws Exception {
        FileInputStream fis = new FileInputStream("/workspace/heapdump.hprof");
        byte[] heap = fis.readAllBytes();
        fis.close();
        
        System.out.println("Heap size: " + heap.length);
        System.out.println("Trying EVERY 16-byte sequence (step 1)...");
        
        int totalTried = 0;
        
        for (int i = 0; i <= heap.length - 16; i++) {
            byte[] key = Arrays.copyOfRange(heap, i, i + 16);
            
            try {
                SecretKeySpec spec = new SecretKeySpec(key, "AES");
                Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
                cipher.init(Cipher.DECRYPT_MODE, spec);
                
                byte[] decrypted = cipher.doFinal(Base64.getDecoder().decode(FLAG.getBytes()));
                String result = new String(decrypted);
                
                if (isPrintableAscii(result) && result.length() >= 15) {
                    System.out.println("\n=== FOUND at offset " + i + " ===");
                    System.out.println(result);
                    System.out.println("Key: " + bytesToHex(key));
                    System.out.println("================================\n");
                }
            } catch (Exception e) {
                // Ignore
            }
            
            totalTried++;
            if (i % 250000 == 0 && i > 0) {
                System.out.println("Progress: " + i + " / " + heap.length);
            }
        }
        
        System.out.println("\nDone. Tried " + totalTried + " keys.");
    }
    
    private static boolean isPrintableAscii(String s) {
        for (char c : s.toCharArray()) {
            if (c < 32 || c > 126) return false;
        }
        return true;
    }
    
    private static String bytesToHex(byte[] bytes) {
        StringBuilder sb = new StringBuilder();
        for (byte b : bytes) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }
}
