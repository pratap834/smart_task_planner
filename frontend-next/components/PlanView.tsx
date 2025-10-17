'use client';

import type { Plan, Task } from '@/types/api';
import { useUpdateTask } from '@/lib/hooks/use-api';
import { formatDate, getTaskColor, getPriorityBadgeColor, calculateProgress } from '@/lib/utils';
import { CheckCircle2, Circle, Clock, AlertCircle } from 'lucide-react';

interface PlanViewProps {
  plan: Plan;
}

export function PlanView({ plan }: PlanViewProps) {
  const updateTask = useUpdateTask(plan.id);
  const progress = calculateProgress(plan.tasks);

  const handleTaskToggle = (taskId: string, currentStatus: boolean) => {
    updateTask.mutate({
      taskId,
      data: { is_completed: !currentStatus },
    });
  };

  const criticalTasks = plan.tasks.filter((t) => plan.critical_path?.includes(t.task_id));
  const nonCriticalTasks = plan.tasks.filter((t) => !plan.critical_path?.includes(t.task_id));

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-xl border border-gray-200 p-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">Project Plan</h2>
        <p className="text-gray-600 mb-6">{plan.plan_summary}</p>

        {/* Progress */}
        <div className="mb-6">
          <div className="flex justify-between text-sm mb-2">
            <span className="font-medium text-gray-700">Overall Progress</span>
            <span className="font-bold text-gray-900">{progress}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div
              className="bg-gradient-to-r from-primary-500 to-primary-600 h-3 rounded-full transition-all"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Stat label="Total Tasks" value={plan.tasks.length.toString()} />
          <Stat label="Completed" value={plan.tasks.filter((t) => t.is_completed).length.toString()} />
          <Stat label="Critical Path" value={plan.critical_path?.length.toString() || '0'} />
          <Stat label="Duration" value={`${plan.total_duration_days || 0} days`} />
        </div>
      </div>

      {/* Critical Path Tasks */}
      {criticalTasks.length > 0 && (
        <div>
          <div className="flex items-center gap-2 mb-4">
            <AlertCircle className="w-5 h-5 text-red-600" />
            <h3 className="text-xl font-bold text-gray-900">Critical Path Tasks</h3>
            <span className="text-sm text-gray-500">(These determine your timeline)</span>
          </div>
          <div className="space-y-3">
            {criticalTasks.map((task) => (
              <TaskCard
                key={task.id}
                task={{ ...task, is_critical: true }}
                onToggle={handleTaskToggle}
              />
            ))}
          </div>
        </div>
      )}

      {/* Other Tasks */}
      {nonCriticalTasks.length > 0 && (
        <div>
          <h3 className="text-xl font-bold text-gray-900 mb-4">Other Tasks</h3>
          <div className="space-y-3">
            {nonCriticalTasks.map((task) => (
              <TaskCard
                key={task.id}
                task={{ ...task, is_critical: false }}
                onToggle={handleTaskToggle}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="text-center">
      <p className="text-2xl font-bold text-gray-900">{value}</p>
      <p className="text-sm text-gray-600">{label}</p>
    </div>
  );
}

function TaskCard({
  task,
  onToggle,
}: {
  task: Task & { is_critical: boolean };
  onToggle: (taskId: string, currentStatus: boolean) => void;
}) {
  const colorClass = getTaskColor(task);

  return (
    <div className={`border-2 rounded-lg p-6 ${colorClass}`}>
      <div className="flex items-start gap-4">
        <button
          onClick={() => onToggle(task.task_id, task.is_completed)}
          className="flex-shrink-0 mt-1 hover:scale-110 transition-transform"
        >
          {task.is_completed ? (
            <CheckCircle2 className="w-6 h-6 text-green-600" />
          ) : (
            <Circle className="w-6 h-6 text-gray-400" />
          )}
        </button>

        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-4 mb-2">
            <h4 className={`font-semibold ${task.is_completed ? 'line-through text-gray-500' : ''}`}>
              {task.task_id}: {task.title}
            </h4>
            <div className="flex items-center gap-2 flex-shrink-0">
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityBadgeColor(task.priority)}`}>
                {task.priority}
              </span>
              {task.is_critical && (
                <span className="px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-700">
                  Critical
                </span>
              )}
            </div>
          </div>

          <p className="text-sm text-gray-700 mb-3">{task.description}</p>

          <div className="flex flex-wrap gap-4 text-sm text-gray-600">
            <div className="flex items-center gap-1">
              <Clock className="w-4 h-4" />
              <span>{task.duration_days} days</span>
            </div>
            <div>
              <span className="font-medium">Start:</span> {formatDate(task.earliest_start)}
            </div>
            <div>
              <span className="font-medium">End:</span> {formatDate(task.latest_finish)}
            </div>
            {task.depends_on && task.depends_on.length > 0 && (
              <div>
                <span className="font-medium">Depends on:</span> {task.depends_on.join(', ')}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
