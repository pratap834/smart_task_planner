'use client';

import type { Plan } from '@/types/api';
import { formatDate, calculateProgress, formatDuration } from '@/lib/utils';
import { Calendar, Clock, Target, TrendingUp, Loader2 } from 'lucide-react';

interface PlanListProps {
  plans: Plan[];
  isLoading: boolean;
  onPlanSelect: (plan: Plan) => void;
}

export function PlanList({ plans, isLoading, onPlanSelect }: PlanListProps) {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
      </div>
    );
  }

  if (plans.length === 0) {
    return (
      <div className="text-center py-12 bg-white rounded-xl border border-gray-200">
        <Target className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-gray-900 mb-2">No plans yet</h3>
        <p className="text-gray-600 mb-6">Create your first plan to get started</p>
      </div>
    );
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {plans.map((plan) => (
        <PlanCard key={plan.id} plan={plan} onClick={() => onPlanSelect(plan)} />
      ))}
    </div>
  );
}

function PlanCard({ plan, onClick }: { plan: Plan; onClick: () => void }) {
  const progress = calculateProgress(plan.tasks);
  const completedTasks = plan.tasks.filter((t) => t.is_completed).length;

  return (
    <button
      onClick={onClick}
      className="w-full text-left bg-white rounded-xl border border-gray-200 p-6 hover:shadow-lg hover:border-primary-300 transition-all group"
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="font-semibold text-gray-900 group-hover:text-primary-600 transition-colors line-clamp-2">
            {plan.plan_summary?.substring(0, 80) || 'Untitled Plan'}
          </h3>
          <p className="text-sm text-gray-500 mt-1">
            Created {formatDate(plan.created_at)}
          </p>
        </div>
      </div>

      <div className="space-y-3">
        {/* Progress Bar */}
        <div>
          <div className="flex justify-between text-sm mb-1">
            <span className="text-gray-600">Progress</span>
            <span className="font-medium text-gray-900">{progress}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-primary-600 h-2 rounded-full transition-all"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 gap-3 pt-3 border-t border-gray-100">
          <div className="flex items-center gap-2 text-sm">
            <Target className="w-4 h-4 text-gray-400" />
            <span className="text-gray-600">
              {completedTasks}/{plan.tasks.length} tasks
            </span>
          </div>
          {plan.total_duration_days && (
            <div className="flex items-center gap-2 text-sm">
              <Clock className="w-4 h-4 text-gray-400" />
              <span className="text-gray-600">
                {formatDuration(plan.total_duration_days)}
              </span>
            </div>
          )}
        </div>

        {/* Critical Path Badge */}
        {plan.critical_path && plan.critical_path.length > 0 && (
          <div className="flex items-center gap-2 text-sm text-red-600 bg-red-50 px-3 py-2 rounded-lg">
            <TrendingUp className="w-4 h-4" />
            <span>{plan.critical_path.length} critical tasks</span>
          </div>
        )}
      </div>
    </button>
  );
}
