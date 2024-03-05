package Zadanie4;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.nio.ByteBuffer;
import java.util.Arrays;

public class JavaUDPServer {
    enum Clients{
        PYTHON,
        JAVA
    }

    public static void main(String[] args){
        System.out.println("JAVA UDP SERVER | ASSIGNMENT 4");

        int portNumber = 9004;

        try ( DatagramSocket socket = new DatagramSocket(portNumber)) {
            byte[] receiveBuffer = new byte[1024];

            while(true){
//              get a new message
                Arrays.fill(receiveBuffer, (byte) 0);
                DatagramPacket receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
                socket.receive(receivePacket);

//              analyze the message
                System.out.printf("%02x %n", receiveBuffer[0]);
                switch (receiveBuffer[0]){
                    case (byte) 0:
                        System.out.println("message from python client");
                        break;
                    case (byte) 255:
                        System.out.println("message from java client");
                        break;
                    default:
                        System.out.println("Unknown client");
                        break;
                }
                System.out.println(new String(receiveBuffer));

            }
        }catch (Exception e){
            e.printStackTrace();
        }

    }
}
