<script>
console.log("hi");

</script>
<?php
require_once 'phpgmailer/class.phpgmailer.php';

$mail = new PHPGMailer();   //object creation

// Check for empty fields
   

$name = $_POST['name'];
$email_address = $_POST['email'];
$phone = $_POST['phone'];
$message = $_POST['message'];

echo $email;  
#if(empty($_POST['name'])      || empty($_POST['email'])     || empty($_POST['phone'])     || empty($_POST['message'])   ||!filter_var($_POST['email'],FILTER_VALIDATE_EMAIL))
#   {
#   echo "No arguments Provided!";
 #  return false;
#   }

// Create the email and send the message
$to = 'koushika26k7@gmail.com'; // Add your email address inbetween the '' replacing yourname@yourdomain.com - This is where the form will send a message to.
$email_subject = "Website Contact Form:  $name";
$email_body = "You have received a new message from your website contact form.\n\n"."Here are the details:\n\nName: $name\n\nEmail: $email_address\n\nPhone: $phone\n\nMessage:\n$message";
$headers = "From: noreply@yourdomain.com\n"; // This is the email address the generated message will be from. We recommend using something like noreply@yourdomain.com.
$headers .= "Reply-To: $email_address";   
$res=mail($to,$email_subject,$email_body,$headers);
echo $res;
return true;         
?>