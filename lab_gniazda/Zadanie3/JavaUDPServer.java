package Zadanie3;

import javax.xml.crypto.Data;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.Arrays;

public class JavaUDPServer {

    public static void main(String args[])
    {
        System.out.println("JAVA UDP SERVER");

        int portNumber = 9003;
        try (DatagramSocket socket = new DatagramSocket(portNumber)) {
            byte[] receiveBuffer = new byte[1024];

            while (true) {
                Arrays.fill(receiveBuffer, (byte) 0);
                DatagramPacket receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
                socket.receive(receivePacket);
                int number = ByteBuffer.wrap(receivePacket.getData()).order(ByteOrder.LITTLE_ENDIAN).getInt();
                System.out.println("received raw number: " + number);

//                send a response
                byte[] sendBuffer = ByteBuffer.allocate(4).putInt(number + 1).array();
                DatagramPacket sendPacket = new DatagramPacket(sendBuffer, sendBuffer.length, receivePacket.getAddress(), receivePacket.getPort());
                socket.send(sendPacket);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    static private void reverse_array(byte[] arr){
        byte buff = 0;
        for (int i = 0; i <= arr.length/2; i++) {
            buff = arr[i];
            arr[i] = arr[arr.length - i -1];
            arr[arr.length -i -1] = buff;
        }
    }
}
