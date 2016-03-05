package mobileRobot.imageProcessing.android.colorDetector;

import android.bluetooth.*;
import android.content.Intent;

import java.io.IOException;
import java.io.OutputStream;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.Set;
import java.util.UUID;

class BTClient
{
    private BluetoothAdapter adap;
    private Set<BluetoothDevice> pairedDevices;
    private BluetoothDevice ev3;

    public BTClient()
    {
        adap = BluetoothAdapter.getDefaultAdapter();


    }

    public Intent startBT()
    {
        return new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
    }

    private BluetoothDevice getEv3()
    {
        //TODO: not elegant, , should configure for each phone

        pairedDevices = adap.getBondedDevices();
        for( BluetoothDevice device : pairedDevices )
        {
            if (device.getName().equals("ev3dev"))
            {
                return device;
            }
        }



        return null;
    }

    public BluetoothSocket connect()
    {
        ev3 = getEv3();
        BluetoothSocket connection = null;
        boolean connected = true;
        try {
            connection = ev3.createRfcommSocketToServiceRecord(UUID.randomUUID());
            connection.connect();
        } catch (IOException e) {
            connected = false;
        }

        if (!connected) {
            Method m = null;
            try {
                m = ev3.getClass().getMethod("createRfcommSocket", new Class[]{int.class});
                connection = (BluetoothSocket) m.invoke(ev3, 1);
                connection.connect();
            } catch (NoSuchMethodException e) {
                return null;
            } catch (InvocationTargetException e) {
                return null;
            } catch (IllegalAccessException e) {
                return null;
            } catch (IOException e) {
                return null;
            }
        }

        return connection;
    }


    public void send(BluetoothSocket connection, String message)
    {
        OutputStream out = null;

        byte[] tbyte = message.getBytes();

        try {
            out = connection.getOutputStream();

            out.write(tbyte);
            out.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public String getDevices()
    {
        pairedDevices = adap.getBondedDevices();

        String devices_string = "> ";

        for( BluetoothDevice device : pairedDevices )
        {
            devices_string = devices_string.concat(device.getName() + " , ");
        }

        return devices_string;
    }
}