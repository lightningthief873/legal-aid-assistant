import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button.jsx";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card.jsx";
import { Textarea } from "@/components/ui/textarea.jsx";
import { Input } from "@/components/ui/input.jsx";
import { Label } from "@/components/ui/label.jsx";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select.jsx";
import { Badge } from "@/components/ui/badge.jsx";
import { Alert, AlertDescription } from "@/components/ui/alert.jsx";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs.jsx";
import { ScrollArea } from "@/components/ui/scroll-area.jsx";
import { Separator } from "@/components/ui/separator.jsx";
import {
  Scale,
  FileText,
  Users,
  AlertCircle,
  CheckCircle,
  Download,
  Send,
  Lightbulb,
  Shield,
  Heart,
  Phone,
  Mail,
  ExternalLink,
  Loader2,
} from "lucide-react";
import "./App.css";

const API_BASE_URL = "http://localhost:8000/api";

function App() {
  const [activeTab, setActiveTab] = useState("submit");
  const [issueData, setIssueData] = useState({
    description: "",
    location: "",
    email: "",
    urgency: "medium",
  });
  const [analysis, setAnalysis] = useState(null);
  const [advice, setAdvice] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [resources, setResources] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentIssueId, setCurrentIssueId] = useState(null);

  useEffect(() => {
    fetchTemplates();
    fetchResources();
  }, []);

  const fetchTemplates = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/templates`);
      if (response.ok) {
        const data = await response.json();
        setTemplates(data);
      }
    } catch (err) {
      console.error("Error fetching templates:", err);
    }
  };

  const fetchResources = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/resources`);
      if (response.ok) {
        const data = await response.json();
        setResources(data);
      }
    } catch (err) {
      console.error("Error fetching resources:", err);
    }
  };

  const handleSubmitIssue = async () => {
    if (!issueData.description.trim()) {
      setError("Please describe your legal issue");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(issueData),
      });

      if (response.ok) {
        const analysisData = await response.json();
        setAnalysis(analysisData);
        setCurrentIssueId(analysisData.issue_id);
        setActiveTab("analysis");
      } else {
        setError("Failed to analyze your issue. Please try again.");
      }
    } catch (err) {
      console.error(
        "Network error. Please check your connection and try again.",
        err
      );
    } finally {
      setLoading(false);
    }
  };

  const handleGetAdvice = async () => {
    if (!currentIssueId) return;

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/advice`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          issue_id: currentIssueId,
        }),
      });

      if (response.ok) {
        const adviceData = await response.json();
        setAdvice(adviceData);
        setActiveTab("advice");
      } else {
        setError("Failed to generate advice. Please try again.");
      }
    } catch (err) {
      console.error(
        "Network error. Please check your connection and try again.",
        err
      );
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateDocument = async (templateId, documentType) => {
    if (!currentIssueId) return;

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/generate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          issue_id: currentIssueId,
          template_id: templateId,
          document_type: documentType,
        }),
      });

      if (response.ok) {
        const docData = await response.json();
        setDocuments((prev) => [...prev, docData]);
        setActiveTab("documents");
      } else {
        setError("Failed to generate document. Please try again.");
      }
    } catch (err) {
      console.error(
        "Network error. Please check your connection and try again.",
        err
      );
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setIssueData({
      description: "",
      location: "",
      email: "",
      urgency: "medium",
    });
    setAnalysis(null);
    setAdvice(null);
    setDocuments([]);
    setCurrentIssueId(null);
    setError(null);
    setActiveTab("submit");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <Scale className="h-8 w-8 text-blue-600" />
              <div>
                <h1 className="text-xl font-bold text-gray-900">
                  Legal Aid Assistant
                </h1>
                <p className="text-sm text-gray-500">
                  AI-Powered Community Legal Support
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <Badge
                variant="secondary"
                className="bg-green-100 text-green-800"
              >
                <Shield className="h-3 w-3 mr-1" />
                Free & Confidential
              </Badge>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <Alert className="mb-6 border-red-200 bg-red-50">
            <AlertCircle className="h-4 w-4 text-red-600" />
            <AlertDescription className="text-red-800">
              {error}
            </AlertDescription>
          </Alert>
        )}

        <Tabs
          value={activeTab}
          onValueChange={setActiveTab}
          className="space-y-6"
        >
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="submit" className="flex items-center space-x-2">
              <FileText className="h-4 w-4" />
              <span>Submit Issue</span>
            </TabsTrigger>
            <TabsTrigger value="analysis" disabled={!analysis}>
              <Lightbulb className="h-4 w-4 mr-2" />
              Analysis
            </TabsTrigger>
            <TabsTrigger value="advice" disabled={!advice}>
              <Heart className="h-4 w-4 mr-2" />
              Advice
            </TabsTrigger>
            <TabsTrigger value="documents">
              <Download className="h-4 w-4 mr-2" />
              Documents
            </TabsTrigger>
            <TabsTrigger value="resources">
              <Users className="h-4 w-4 mr-2" />
              Resources
            </TabsTrigger>
          </TabsList>

          {/* Submit Issue Tab */}
          <TabsContent value="submit" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <FileText className="h-5 w-5 text-blue-600" />
                  <span>Describe Your Legal Issue</span>
                </CardTitle>
                <CardDescription>
                  Provide details about your legal situation. Our AI will
                  analyze your issue and provide guidance.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="description">Issue Description *</Label>
                  <Textarea
                    id="description"
                    placeholder="Please describe your legal issue in detail. Include relevant dates, parties involved, and any actions taken so far..."
                    value={issueData.description}
                    onChange={(e) =>
                      setIssueData((prev) => ({
                        ...prev,
                        description: e.target.value,
                      }))
                    }
                    className="min-h-32"
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="location">Location (State/City)</Label>
                    <Input
                      id="location"
                      placeholder="e.g., California, New York City"
                      value={issueData.location}
                      onChange={(e) =>
                        setIssueData((prev) => ({
                          ...prev,
                          location: e.target.value,
                        }))
                      }
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="urgency">Urgency Level</Label>
                    <Select
                      value={issueData.urgency}
                      onValueChange={(value) =>
                        setIssueData((prev) => ({ ...prev, urgency: value }))
                      }
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="low">
                          Low - General inquiry
                        </SelectItem>
                        <SelectItem value="medium">
                          Medium - Important matter
                        </SelectItem>
                        <SelectItem value="high">
                          High - Urgent situation
                        </SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="email">Email (Optional)</Label>
                  <Input
                    id="email"
                    type="email"
                    placeholder="your.email@example.com"
                    value={issueData.email}
                    onChange={(e) =>
                      setIssueData((prev) => ({
                        ...prev,
                        email: e.target.value,
                      }))
                    }
                  />
                </div>

                <Button
                  onClick={handleSubmitIssue}
                  disabled={loading || !issueData.description.trim()}
                  className="w-full"
                >
                  {loading ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Send className="h-4 w-4 mr-2" />
                      Analyze My Issue
                    </>
                  )}
                </Button>

                <div className="text-sm text-gray-500 bg-gray-50 p-3 rounded-lg">
                  <p className="font-medium mb-1">Important Disclaimer:</p>
                  <p>
                    This tool provides general legal information only and is not
                    a substitute for professional legal advice. For specific
                    legal matters, please consult with a qualified attorney.
                  </p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Analysis Tab */}
          <TabsContent value="analysis" className="space-y-6">
            {analysis && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Lightbulb className="h-5 w-5 text-yellow-600" />
                    <span>Issue Analysis</span>
                  </CardTitle>
                  <CardDescription>
                    AI analysis of your legal issue with categorization and
                    initial guidance.
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="text-center p-4 bg-blue-50 rounded-lg">
                      <p className="text-sm text-gray-600">Category</p>
                      <p className="font-semibold text-blue-800 capitalize">
                        {analysis.category?.replace("_", " ")}
                      </p>
                    </div>
                    <div className="text-center p-4 bg-green-50 rounded-lg">
                      <p className="text-sm text-gray-600">Confidence</p>
                      <p className="font-semibold text-green-800">
                        {Math.round(analysis.confidence * 100)}%
                      </p>
                    </div>
                    <div className="text-center p-4 bg-orange-50 rounded-lg">
                      <p className="text-sm text-gray-600">Complexity</p>
                      <p className="font-semibold text-orange-800 capitalize">
                        {analysis.estimated_complexity}
                      </p>
                    </div>
                  </div>

                  {analysis.suggested_actions &&
                    analysis.suggested_actions.length > 0 && (
                      <div>
                        <h4 className="font-semibold mb-2">
                          Suggested Next Steps:
                        </h4>
                        <ul className="space-y-2">
                          {analysis.suggested_actions.map((action, index) => (
                            <li
                              key={index}
                              className="flex items-start space-x-2"
                            >
                              <CheckCircle className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                              <span className="text-sm">{action}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                  <div className="flex space-x-3">
                    <Button onClick={handleGetAdvice} disabled={loading}>
                      {loading ? (
                        <>
                          <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                          Generating...
                        </>
                      ) : (
                        <>
                          <Heart className="h-4 w-4 mr-2" />
                          Get Detailed Advice
                        </>
                      )}
                    </Button>
                    <Button variant="outline" onClick={resetForm}>
                      Start Over
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* Advice Tab */}
          <TabsContent value="advice" className="space-y-6">
            {advice && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Heart className="h-5 w-5 text-red-600" />
                    <span>Legal Guidance</span>
                  </CardTitle>
                  <CardDescription>
                    Detailed advice and recommendations for your situation.
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="prose max-w-none">
                    <p className="text-gray-700 leading-relaxed">
                      {advice.advice}
                    </p>
                  </div>

                  {advice.next_steps && advice.next_steps.length > 0 && (
                    <div>
                      <h4 className="font-semibold mb-2">
                        Recommended Actions:
                      </h4>
                      <ol className="space-y-2">
                        {advice.next_steps.map((step, index) => (
                          <li
                            key={index}
                            className="flex items-start space-x-2"
                          >
                            <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-1 rounded-full mt-0.5">
                              {index + 1}
                            </span>
                            <span className="text-sm">{step}</span>
                          </li>
                        ))}
                      </ol>
                    </div>
                  )}

                  {advice.relevant_laws && advice.relevant_laws.length > 0 && (
                    <div>
                      <h4 className="font-semibold mb-2">
                        Relevant Laws & Regulations:
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        {advice.relevant_laws.map((law, index) => (
                          <Badge key={index} variant="secondary">
                            {law}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  )}

                  <Separator />

                  <div className="text-sm text-gray-500 bg-yellow-50 p-3 rounded-lg border border-yellow-200">
                    <p className="font-medium text-yellow-800 mb-1">
                      Legal Disclaimer:
                    </p>
                    <p className="text-yellow-700">
                      This information is for educational purposes only and does
                      not constitute legal advice. Consult with a qualified
                      attorney for advice specific to your situation.
                    </p>
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* Documents Tab */}
          <TabsContent value="documents" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Download className="h-5 w-5 text-green-600" />
                  <span>Legal Documents</span>
                </CardTitle>
                <CardDescription>
                  Generate and download legal documents based on your issue.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {templates.length > 0 && (
                  <div>
                    <h4 className="font-semibold mb-3">Available Templates:</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {templates.map((template) => (
                        <div
                          key={template.id}
                          className="border rounded-lg p-3 hover:bg-gray-50"
                        >
                          <h5 className="font-medium">{template.name}</h5>
                          <p className="text-sm text-gray-600 mb-2">
                            {template.description}
                          </p>
                          <Button
                            size="sm"
                            onClick={() =>
                              handleGenerateDocument(
                                template.id,
                                "demand_letter"
                              )
                            }
                            disabled={!currentIssueId || loading}
                          >
                            Generate Document
                          </Button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {documents.length > 0 && (
                  <div>
                    <h4 className="font-semibold mb-3">Generated Documents:</h4>
                    <div className="space-y-2">
                      {documents.map((doc) => (
                        <div
                          key={doc.id}
                          className="flex items-center justify-between p-3 border rounded-lg"
                        >
                          <div>
                            <p className="font-medium">{doc.file_name}</p>
                            <p className="text-sm text-gray-600">
                              Generated on{" "}
                              {new Date(doc.generated_at).toLocaleDateString()}
                            </p>
                          </div>
                          <Button size="sm" asChild>
                            <a
                              href={`${API_BASE_URL}${doc.download_url}`}
                              target="_blank"
                              rel="noopener noreferrer"
                            >
                              <Download className="h-4 w-4 mr-2" />
                              Download
                            </a>
                          </Button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {documents.length === 0 && (
                  <div className="text-center py-8 text-gray-500">
                    <FileText className="h-12 w-12 mx-auto mb-3 text-gray-300" />
                    <p>No documents generated yet.</p>
                    <p className="text-sm">
                      Submit an issue and get advice to generate relevant
                      documents.
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Resources Tab */}
          <TabsContent value="resources" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Users className="h-5 w-5 text-purple-600" />
                  <span>Legal Resources</span>
                </CardTitle>
                <CardDescription>
                  Find local legal aid organizations and helpful resources.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ScrollArea className="h-96">
                  <div className="space-y-4">
                    {resources.map((resource) => (
                      <div
                        key={resource.id}
                        className="border rounded-lg p-4 hover:bg-gray-50"
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <h4 className="font-semibold text-lg">
                              {resource.name}
                            </h4>
                            <p className="text-sm text-gray-600 mb-2">
                              {resource.description}
                            </p>

                            <div className="flex flex-wrap gap-2 mb-3">
                              {resource.categories?.map((category, index) => (
                                <Badge
                                  key={index}
                                  variant="outline"
                                  className="text-xs"
                                >
                                  {category.replace("_", " ")}
                                </Badge>
                              ))}
                            </div>

                            <div className="space-y-1 text-sm">
                              {resource.phone && (
                                <div className="flex items-center space-x-2">
                                  <Phone className="h-4 w-4 text-gray-400" />
                                  <span>{resource.phone}</span>
                                </div>
                              )}
                              {resource.email && (
                                <div className="flex items-center space-x-2">
                                  <Mail className="h-4 w-4 text-gray-400" />
                                  <span>{resource.email}</span>
                                </div>
                              )}
                              {resource.website && (
                                <div className="flex items-center space-x-2">
                                  <ExternalLink className="h-4 w-4 text-gray-400" />
                                  <a
                                    href={resource.website}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="text-blue-600 hover:underline"
                                  >
                                    Visit Website
                                  </a>
                                </div>
                              )}
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </ScrollArea>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-sm text-gray-500">
            <p>
              © 2024 AI-Backed Community Legal Aid Assistant. This tool provides
              general legal information only.
            </p>
            <p className="mt-1">
              Always consult with a qualified attorney for legal advice specific
              to your situation.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
