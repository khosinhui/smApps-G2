package com.example.login;


import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.jar.Attributes;

public class TopupActivity extends AppCompatActivity {

    private EditText number;
    private Button topup;

    private TextView profileBalance, profileName;
    int finalbalance;
    String credit;
    private FirebaseAuth firebaseAuth;
    private FirebaseDatabase firebaseDatabase;





    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_topup);

        number=findViewById(R.id.etNum);
        topup=findViewById(R.id.btnTopup);
        profileBalance=findViewById(R.id.tvTopupbalance);
        profileName=findViewById(R.id.tvprofileName);

        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        firebaseAuth = FirebaseAuth.getInstance();
        firebaseDatabase = FirebaseDatabase.getInstance();
        DatabaseReference databaseReference = FirebaseDatabase.getInstance().getReference(firebaseAuth.getUid());
        databaseReference.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                String name = dataSnapshot.child("Name").getValue().toString();
                String balance = dataSnapshot.child("Balance").getValue().toString();

                profileName.setText("UserName: " + name);
                profileBalance.setText("Topup Balance is: RM" + balance);

                finalbalance = Integer.parseInt(balance);
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {
                Toast.makeText(TopupActivity.this, databaseError.getCode(), Toast.LENGTH_SHORT).show();

            }
        });

        topup.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                FirebaseDatabase firebaseDatabase = FirebaseDatabase.getInstance();
                DatabaseReference databaseReference = firebaseDatabase.getReference(firebaseAuth.getUid());

                if(validate()){
                    //Upload data to the database


                int number1 = Integer.parseInt(number.getText().toString());
                int temp = number1;
                finalbalance +=number1;

                profileBalance.setText("Topup Balance is: RM " + String.valueOf(finalbalance));

                databaseReference.child("Balance").setValue(finalbalance);

            }}
        });






    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {

        switch (item.getItemId()){
            case android.R.id.home:
                onBackPressed();
        }
        return super.onOptionsItemSelected(item);
    }

    private Boolean validate (){
        Boolean result = false;


        credit = number.getText().toString();
        if(credit.isEmpty()) {
            Toast.makeText(this, "Please enter your desired credit", Toast.LENGTH_SHORT).show();
        }else {
            result = true;
        }
        return result;
    }
}
