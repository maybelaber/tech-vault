import { Card, CardContent } from "../components/ui/Card";

export default function Recommendations() {
  return (
    <div className="py-6">
      <h2 className="text-lg font-semibold text-slate-100 mb-1">Recommendations</h2>
      <p className="text-slate-400 text-sm mb-4">
        Top resources for your skill level — highest average rating.
      </p>
      <Card className="p-4">
        <CardContent className="p-0 text-slate-400 text-sm text-center py-8">
          Placeholder: recommendations list
        </CardContent>
      </Card>
    </div>
  );
}
