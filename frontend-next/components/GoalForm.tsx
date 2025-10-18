'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useGeneratePlan } from '@/lib/hooks/use-api';
import { Loader2, Sparkles } from 'lucide-react';

const goalSchema = z.object({
  goal_text: z.string().min(20, 'Goal must be at least 20 characters').max(500),
  deadline: z.string().optional(),
  max_hours_per_day: z.number().min(1).max(24).optional(),
  no_work_on_weekends: z.boolean().optional(),
  plan_type: z.enum(['aggressive', 'moderate', 'conservative']).default('moderate'),
});

type GoalFormData = z.infer<typeof goalSchema>;

interface GoalFormProps {
  onSuccess?: (plan: any) => void;
}

export function GoalForm({ onSuccess }: GoalFormProps) {
  const [unavailableDates, setUnavailableDates] = useState<string[]>([]);
  const [dateInput, setDateInput] = useState('');

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<GoalFormData>({
    resolver: zodResolver(goalSchema),
    defaultValues: {
      plan_type: 'moderate',
      max_hours_per_day: 8,
      no_work_on_weekends: true,
    },
  });

  const generatePlan = useGeneratePlan();

  const onSubmit = (data: GoalFormData) => {
    generatePlan.mutate(
      {
        ...data,
        unavailable_dates: unavailableDates.length > 0 ? unavailableDates : undefined,
      },
      {
        onSuccess: (plan) => {
          onSuccess?.(plan);
        },
      }
    );
  };

  const addUnavailableDate = () => {
    if (dateInput && !unavailableDates.includes(dateInput)) {
      setUnavailableDates([...unavailableDates, dateInput]);
      setDateInput('');
    }
  };

  const removeUnavailableDate = (date: string) => {
    setUnavailableDates(unavailableDates.filter((d) => d !== date));
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      {/* Goal Text */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          What do you want to accomplish? *
        </label>
        <textarea
          {...register('goal_text')}
          rows={4}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
          placeholder="e.g., Build a full-stack e-commerce website with payment integration, user authentication, and admin dashboard"
        />
        {errors.goal_text && (
          <p className="mt-1 text-sm text-red-600">{errors.goal_text.message}</p>
        )}
      </div>

      {/* Plan Type */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Plan Type
        </label>
        <select
          {...register('plan_type')}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        >
          <option value="aggressive">Aggressive (Fast, 8-9 tasks)</option>
          <option value="moderate">Moderate (Balanced, 10-12 tasks)</option>
          <option value="conservative">Conservative (Detailed, 12-15 tasks)</option>
        </select>
      </div>

      {/* Deadline */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Deadline (Optional)
        </label>
        <input
          type="date"
          {...register('deadline')}
          min={new Date().toISOString().split('T')[0]}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        />
      </div>

      {/* Max Hours Per Day */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Max Hours Per Day
        </label>
        <input
          type="number"
          {...register('max_hours_per_day', { valueAsNumber: true })}
          min={1}
          max={24}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        />
      </div>

      {/* Work on Weekends */}
      <div className="flex items-center gap-3">
        <input
          type="checkbox"
          {...register('no_work_on_weekends')}
          className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
        />
        <label className="text-sm font-medium text-gray-700">
          No work on weekends
        </label>
      </div>

      {/* Unavailable Dates */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Unavailable Dates (Holidays, Vacations)
        </label>
        <div className="flex gap-2">
          <input
            type="date"
            value={dateInput}
            onChange={(e) => setDateInput(e.target.value)}
            min={new Date().toISOString().split('T')[0]}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
          <button
            type="button"
            onClick={addUnavailableDate}
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
          >
            Add
          </button>
        </div>
        {unavailableDates.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-2">
            {unavailableDates.map((date) => (
              <span
                key={date}
                className="inline-flex items-center gap-2 px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm"
              >
                {new Date(date).toLocaleDateString()}
                <button
                  type="button"
                  onClick={() => removeUnavailableDate(date)}
                  className="text-gray-500 hover:text-red-600"
                >
                  ×
                </button>
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={generatePlan.isPending}
        className="w-full flex items-center justify-center gap-2 bg-primary-600 text-white px-6 py-3 rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium"
      >
        {generatePlan.isPending ? (
          <>
            <Loader2 className="w-5 h-5 animate-spin" />
            Generating Plan with AI...
          </>
        ) : (
          <>
            <Sparkles className="w-5 h-5" />
            Generate Plan
          </>
        )}
      </button>

      {generatePlan.isError && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-800">
          <p className="font-medium">Error generating plan</p>
          <p className="text-sm mt-1">{generatePlan.error?.message || 'Please try again'}</p>
        </div>
      )}
    </form>
  );
}
