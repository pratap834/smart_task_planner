'use client';

import { useState } from 'react';
import { usePlans } from '@/lib/hooks/use-api';
import { GoalForm } from '@/components/GoalForm';
import { PlanList } from '@/components/PlanList';
import { PlanView } from '@/components/PlanView';
import { Target, Plus, List } from 'lucide-react';
import type { Plan } from '@/types/api';

export default function DashboardPage() {
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState<Plan | null>(null);
  const { data: plans, isLoading, refetch } = usePlans();

  const handlePlanCreated = async (plan: any) => {
    setShowCreateForm(false);
    // Refresh the plans list
    await refetch();
    // Show the newly created plan
    setSelectedPlan(plan);
  };

  const handlePlanSelect = (plan: Plan) => {
    setSelectedPlan(plan);
  };

  const handleBack = () => {
    if (selectedPlan) {
      setSelectedPlan(null);
    } else {
      setShowCreateForm(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b sticky top-0 z-40 shadow-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Target className="w-8 h-8 text-primary-600" />
              <h1 className="text-2xl font-bold text-gray-900">Smart Task Planner</h1>
            </div>
            {!showCreateForm && !selectedPlan && (
              <button
                onClick={() => setShowCreateForm(true)}
                className="flex items-center gap-2 bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors shadow-sm"
              >
                <Plus className="w-5 h-5" />
                New Plan
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {showCreateForm ? (
          <div className="max-w-3xl mx-auto">
            <div className="mb-6">
              <button
                onClick={handleBack}
                className="text-gray-600 hover:text-gray-900 flex items-center gap-2"
              >
                ← Back to Plans
              </button>
            </div>
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
              <div className="flex items-center gap-3 mb-6">
                <Plus className="w-6 h-6 text-primary-600" />
                <h2 className="text-2xl font-bold text-gray-900">Create New Plan</h2>
              </div>
              <GoalForm onSuccess={handlePlanCreated} />
            </div>
          </div>
        ) : selectedPlan ? (
          <div>
            <div className="mb-6">
              <button
                onClick={handleBack}
                className="text-gray-600 hover:text-gray-900 flex items-center gap-2"
              >
                ← Back to Plans
              </button>
            </div>
            <PlanView plan={selectedPlan} />
          </div>
        ) : (
          <div>
            <div className="flex items-center gap-3 mb-6">
              <List className="w-6 h-6 text-gray-700" />
              <h2 className="text-2xl font-bold text-gray-900">Your Plans</h2>
            </div>
            <PlanList
              plans={plans || []}
              isLoading={isLoading}
              onPlanSelect={handlePlanSelect}
            />
          </div>
        )}
      </main>
    </div>
  );
}
