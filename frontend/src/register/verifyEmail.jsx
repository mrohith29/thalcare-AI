export default function VerifyEmail() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4 flex items-center justify-center">
      <div className="w-full max-w-lg bg-white rounded-3xl shadow-xl p-10 text-center">
        <div className="mx-auto mb-6 w-20 h-20 rounded-full bg-blue-100 flex items-center justify-center">
          <span className="text-3xl">📧</span>
        </div>
        <h1 className="text-2xl font-bold text-gray-900">Check your email</h1>
        <p className="mt-3 text-gray-600">
          We sent you a verification link. Please verify your email address to complete your account setup.
        </p>
        <div className="mt-8 text-sm text-gray-500">
          <p>
            Didn’t receive the email? Check your spam folder or try again.
          </p>
        </div>
        <div className="mt-8">
          <a href="/login" className="inline-block px-6 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold shadow hover:from-blue-700 hover:to-indigo-700">
            Back to Sign in
          </a>
        </div>
      </div>
    </div>
  );
}


