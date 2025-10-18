import java.io.*;
import java.util.*;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class BruteDecrypt {
    public static final String FLAG = "S+kUZtaHEYpFpv2ixuTnqBdORNzsdVJrAxWznyOljEo=";
    
    public static void main(String[] args) throws Exception {
        // Read the heap dump
        FileInputStream fis = new FileInputStream("/workspace/heapdump.hprof");
        byte[] heap = fis.readAllBytes();
        fis.close();
        
        System.out.println("Heap size: " + heap.length + " bytes");
        System.out.println("Trying to decrypt with all 16-byte sequences...");
        
        Set<String> tried = new HashSet<>();
        int count = 0;
        
        // Try every 16-byte sequence as a potential AES key
        for (int i = 0; i <= heap.length - 16; i++) {
            byte[] key = Arrays.copyOfRange(heap, i, i + 16);
            
            // Convert to hex string for deduplication
            String keyHex = bytesToHex(key);
            if (tried.contains(keyHex)) {
                continue;
            }
            tried.add(keyHex);
            
            try {
                SecretKeySpec spec = new SecretKeySpec(key, "AES");
                Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
                cipher.init(Cipher.DECRYPT_MODE, spec);
                
                byte[] decrypted = cipher.doFinal(Base64.getDecoder().decode(FLAG.getBytes()));
                String result = new String(decrypted);
                
                // Check if result is printable ASCII
                if (isPrintableAscii(result)) {
                    System.out.println("FOUND AT OFFSET " + i + ": " + result);
                    System.out.println("Key (hex): " + keyHex);
                }
            } catch (Exception e) {
                // Ignore decryption failures
            }
            
            count++;
            if (count % 100000 == 0) {
                System.out.println("Tried " + count + " unique keys, offset " + i + "...");
            }
        }
        
        System.out.println("Done. Tried " + count + " unique keys.");
    }
    
    private static boolean isPrintableAscii(String s) {
        if (s.length() < 10 || s.length() > 100) return false;
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
