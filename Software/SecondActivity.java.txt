package com.example.login;

import android.Manifest;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Vibrator;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.SparseArray;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.vision.CameraSource;
import com.google.android.gms.vision.Detector;
import com.google.android.gms.vision.barcode.Barcode;
import com.google.android.gms.vision.barcode.BarcodeDetector;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class SecondActivity extends AppCompatActivity {

    private FirebaseAuth firebaseAuth;

    private SurfaceView surfaceView;
    private CameraSource cameraSource;
    private BarcodeDetector barcodeDetector;
    private TextView code;
    public TextView Wallet;
    public DatabaseReference databaseReference;

    public String message;

    int currentbalance1;





    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_second);

        firebaseAuth = FirebaseAuth.getInstance();
        FirebaseDatabase firebaseDatabase = FirebaseDatabase.getInstance();
        databaseReference = FirebaseDatabase.getInstance().getReference();
        setupUIViews2();

        qrScanner();


        databaseReference.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                String balance = dataSnapshot.child(firebaseAuth.getUid()).child("Balance").getValue().toString();

                currentbalance1 = Integer.parseInt(balance);
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {
                Toast.makeText(SecondActivity.this, databaseError.getCode(), Toast.LENGTH_SHORT).show();

            }
        });


        Wallet.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(SecondActivity.this, TopupActivity.class));
            }
        });


    }


    private void setupUIViews2()
    {
        surfaceView = (SurfaceView)findViewById(R.id.svCamera);
        code = (TextView)findViewById(R.id.tvCode);
        Wallet=(TextView)findViewById(R.id.tvWallet);

        barcodeDetector = new BarcodeDetector.Builder(this)
                .setBarcodeFormats(Barcode.QR_CODE).build();
        cameraSource = new CameraSource.Builder(this, barcodeDetector)
                .setRequestedPreviewSize(1024, 1024).setAutoFocusEnabled(true).build();
    }

    private void qrScanner()
    {
        surfaceView.getHolder().addCallback(new SurfaceHolder.Callback() {
            @Override
            public void surfaceCreated(SurfaceHolder holder) {
                if (ActivityCompat.checkSelfPermission(getApplicationContext(), Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
                    return;
                }

                try
                {
                    cameraSource.start(holder);
                }catch(IOException e)
                {
                    e.printStackTrace();
                }

            }

            @Override
            public void surfaceChanged(SurfaceHolder holder, int format, int width, int height) {

            }

            @Override
            public void surfaceDestroyed(SurfaceHolder holder) {
                cameraSource.stop();

            }
        });

        barcodeDetector.setProcessor(new Detector.Processor<Barcode>() {
            @Override
            public void release() {

            }

            @Override
            public void receiveDetections(Detector.Detections<Barcode> detections) {
                final SparseArray<Barcode> qrCodes = detections.getDetectedItems();

                if (qrCodes.size()!=0)
                {
                    code.post(new Runnable() {
                        @Override
                        public void run() {
                            Vibrator vibrator = (Vibrator)getApplicationContext().getSystemService(Context.VIBRATOR_SERVICE);
                            vibrator.vibrate(1000);

                        message = qrCodes.valueAt(0).rawValue;
//                        System.out.println(message);

                        code.setText(message);

                if (message.equals("1234"))
                {

                    Map<String, Object> data = new HashMap<>();
                    data.put("servo_in", true );
                    databaseReference.child("Barrier").updateChildren(data);

                }
                if (message.equals("4321"))
                {
                    Map<String, Object> data = new HashMap<>();
                    data.put("servo_out", true );
                    databaseReference.child("Barrier").updateChildren(data);

                    int deductbalance = 5;
                    currentbalance1 -= deductbalance;
                    databaseReference.child(firebaseAuth.getUid()).child("Balance").setValue(currentbalance1);
                    cameraSource.release();
                    finish();
                    startActivity(new Intent(SecondActivity.this, SeeyouActivity.class));



                }


                        }
                    });
                }

            }
        });
    }
    
    
    
    private void Logout(){
        firebaseAuth.signOut();
        finish();
        startActivity(new Intent(SecondActivity.this, MainActivity.class));
    }

    private void Topup()
    {
        startActivity(new Intent(SecondActivity.this, TopupActivity.class));
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.menu, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {

        switch(item.getItemId()){
            case R.id.topupMenu:
                Topup();
                return true;

            case R.id.logoutMenu:
                Logout();
                return true;



                default:
                    return super.onOptionsItemSelected(item);

        }

    }
}
