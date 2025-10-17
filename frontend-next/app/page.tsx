import Link from 'next/link';
import { ArrowRight, CheckCircle2, Target, Zap } from 'lucide-react';

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <Target className="w-8 h-8 text-primary-600" />
            <h1 className="text-2xl font-bold text-gray-900">Smart Task Planner</h1>
          </div>
          <Link
            href="/dashboard"
            className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition-colors"
          >
            Get Started
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="text-center max-w-4xl mx-auto">
          <h2 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Turn Your Goals Into
            <span className="text-primary-600"> Actionable Plans</span>
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            AI-powered project planning that generates detailed task breakdowns, identifies dependencies,
            calculates critical paths, and schedules timelines automatically.
          </p>
          <Link
            href="/dashboard"
            className="inline-flex items-center gap-2 bg-primary-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-primary-700 transition-colors shadow-lg hover:shadow-xl"
          >
            Create Your First Plan
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>

      {/* Features */}
      <section className="container mx-auto px-4 py-20">
        <h3 className="text-3xl font-bold text-center text-gray-900 mb-12">
          Powerful Features
        </h3>
        <div className="grid md:grid-cols-3 gap-8">
          <FeatureCard
            icon={<Zap className="w-12 h-12 text-primary-600" />}
            title="AI-Powered Generation"
            description="Google Gemini AI analyzes your goals and generates comprehensive task breakdowns in seconds."
          />
          <FeatureCard
            icon={<CheckCircle2 className="w-12 h-12 text-success-600" />}
            title="Critical Path Analysis"
            description="Automatically identifies tasks that determine your project timeline and prioritizes accordingly."
          />
          <FeatureCard
            icon={<Target className="w-12 h-12 text-purple-600" />}
            title="Smart Scheduling"
            description="Respects deadlines, work hours, weekends, and dependencies to create realistic timelines."
          />
        </div>
      </section>

      {/* How It Works */}
      <section className="bg-white py-20">
        <div className="container mx-auto px-4">
          <h3 className="text-3xl font-bold text-center text-gray-900 mb-12">
            How It Works
          </h3>
          <div className="max-w-3xl mx-auto space-y-8">
            <Step
              number="1"
              title="Enter Your Goal"
              description="Describe what you want to achieve - from building an app to launching a business."
            />
            <Step
              number="2"
              title="Set Constraints"
              description="Add deadlines, work hours, and preferences. The AI respects your constraints."
            />
            <Step
              number="3"
              title="Get Your Plan"
              description="Receive a detailed breakdown with tasks, dependencies, timelines, and critical path."
            />
            <Step
              number="4"
              title="Track Progress"
              description="Mark tasks complete, visualize progress, and stay on track to meet your goals."
            />
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="container mx-auto px-4 py-20 text-center">
        <div className="bg-gradient-to-r from-primary-600 to-purple-600 rounded-2xl p-12 text-white">
          <h3 className="text-4xl font-bold mb-4">Ready to Start Planning?</h3>
          <p className="text-xl mb-8 opacity-90">
            Join thousands of users who plan smarter with AI
          </p>
          <Link
            href="/dashboard"
            className="inline-flex items-center gap-2 bg-white text-primary-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-gray-100 transition-colors shadow-lg"
          >
            Create Your First Plan
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t bg-gray-50 py-8">
        <div className="container mx-auto px-4 text-center text-gray-600">
          <p>© 2025 Smart Task Planner. Powered by Google Gemini AI.</p>
        </div>
      </footer>
    </main>
  );
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode; title: string; description: string }) {
  return (
    <div className="bg-white p-8 rounded-xl shadow-sm hover:shadow-md transition-shadow border border-gray-100">
      <div className="mb-4">{icon}</div>
      <h4 className="text-xl font-semibold text-gray-900 mb-2">{title}</h4>
      <p className="text-gray-600">{description}</p>
    </div>
  );
}

function Step({ number, title, description }: { number: string; title: string; description: string }) {
  return (
    <div className="flex gap-6">
      <div className="flex-shrink-0 w-12 h-12 rounded-full bg-primary-600 text-white flex items-center justify-center text-xl font-bold">
        {number}
      </div>
      <div>
        <h4 className="text-xl font-semibold text-gray-900 mb-2">{title}</h4>
        <p className="text-gray-600">{description}</p>
      </div>
    </div>
  );
}
