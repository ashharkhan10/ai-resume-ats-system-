/**
 * Sign-up page ( /register ).
 * Colourful panel on the left (big screens only), form on the right.
 */
import { Header } from "@/components/layout/Header";
import { AuthForm } from "@/components/auth/AuthForm";
import { AuthShowcase } from "@/components/auth/AuthShowcase";

export default function RegisterPage() {
  return (
    <>
      <Header />
      <main className="mx-auto grid w-full max-w-6xl flex-1 items-stretch gap-6 px-4 pb-16 lg:grid-cols-2">
        <AuthShowcase />
        <div className="flex items-center justify-center">
          <AuthForm mode="register" />
        </div>
      </main>
    </>
  );
}
